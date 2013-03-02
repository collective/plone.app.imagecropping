from Acquisition import aq_base
from OFS.Image import Pdata
from Products.Five.browser import BrowserView
from ZODB.blob import Blob
from cStringIO import StringIO
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping import HAS_DEXTERITY
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.app.imaging.utils import getAllowedSizes
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from zope.annotation.interfaces import IAnnotations
import PIL.Image
import time


class CroppingView(BrowserView):

    DEFAULT_FORMAT = 'PNG'

    def __call__(self, **kw):
        rq = self.request
        box = (rq['x1'], rq['y1'], rq['x2'], rq['y2'])

        self._crop(rq['fieldname'], rq['scale'], box)

        return True

    def now_millis(self):
        return int(time.time() * 1000)

    def _crop(self, fieldname, scale, box, interface=None):
        """switch between dexterity and Archetypes
        """
        if HAS_DEXTERITY:
            field = getattr(self.context, fieldname)
            data = field.data
        else:
            field = self.context.getField(fieldname)
            handler = IImageScaleHandler(field)

            value = field.get(self.context)
            data = getattr(aq_base(value), 'data', value)
            if isinstance(data, Pdata):
                data = str(data)

        original_file = StringIO(data)
        image = PIL.Image.open(original_file)
        image_format = image.format or self.DEFAULT_FORMAT

        cropped_image = image.crop(box)
        cropped_image_file = StringIO()
        cropped_image.save(cropped_image_file, image_format, quality=100)
        cropped_image_file.seek(0)

        if HAS_DEXTERITY:
            self._dexterity_crop(
                fieldname, field, scale, cropped_image_file, interface)
        else:
            self._atct_crop(
                field, scale, cropped_image_file, handler, interface)

        # store crop information in annotations
        self._store(fieldname, scale, box)

    def _dexterity_crop(self, fieldname, field, scale, image_file, interface):
        """ Cropping for dexterity
        """
        sizes = getAllowedSizes()
        w, h = sizes[scale]

        def crop_factory(fieldname, **parameters):
            result = scaleImage(image_file.read(), **parameters)
            if result is not None:
                data, format, dimensions = result
                mimetype = 'image/%s' % format.lower()
                value = field.__class__(
                    data,
                    contentType=mimetype,
                    filename=field.filename
                )
                value.fieldname = fieldname
                return value, format, dimensions

        # call storage with actual time in milliseconds
        # this always invalidates old scales
        storage = AnnotationStorage(self.context, self.now_millis)

        # We need to pass direction='thumbnail' since this is the default
        # used by plone.namedfile.scaling, also for retrieval of scales.
        # Otherwise the key under which the scaled and cropped image is saved
        # in plone.scale.storage.AnnotationStorage will not match the key used
        # for retrieval (= the cropped scaled image will not be found)
        storage.scale(
            factory=crop_factory,
            direction='thumbnail',
            fieldname=fieldname,
            width=w,
            height=h,
        )

    def _atct_crop(self, field, scale, image_file, handler, interface):
        """ Cropping for Archetypes
        """
        sizes = field.getAvailableSizes(self.context)
        w, h = sizes[scale]
        data = handler.createScale(
            self.context, scale, w, h, data=image_file.read())

        # store scale for classic <fieldname>_<scale> traversing
        handler.storeScale(self.context, scale, **data)

        # call plone.scale.storage.scale method in order to
        # provide saved scale for plone.app.imaging @@images view
        def crop_factory(fieldname, direction='keep', **parameters):
            blob = Blob()
            result = blob.open('w')
            _, image_format, dimensions = scaleImage(
                data['data'], result=result, **parameters)
            result.close()
            return blob, image_format, dimensions

        # call storage with actual time in milliseconds
        # this always invalidates old scales
        storage = AnnotationStorage(self.context, self.now_millis)
        storage.scale(
            factory=crop_factory, fieldname=field.__name__, width=w, height=h)

    @property
    def _storage(self):
        return IAnnotations(self.context).setdefault(
            PAI_STORAGE_KEY, PersistentDict())

    def _store(self, fieldname, scale, box):
        self._storage["%s_%s" % (fieldname, scale)] = box
        return True

    def _read(self, fieldname, scale):
        return self._storage.get('%s_%s' % (fieldname, scale))

    def _remove(self, fieldname, scale):
        # remove info from annotation
        key = "%s_%s" % (fieldname, scale)
        if key in self._storage.keys():
            del self._storage[key]

        # remove saved scale
        scale_storage = AnnotationStorage(self.context)
        image_scales = self.context.restrictedTraverse("@@images")
        image_scale = image_scales.scale(fieldname, scale=scale)
        del scale_storage[image_scale.uid]
