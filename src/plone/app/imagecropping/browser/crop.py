from Acquisition import aq_base
from OFS.Image import Pdata
from Products.Five.browser import BrowserView
from ZODB.blob import Blob
from cStringIO import StringIO
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imaging.interfaces import IImageScaleHandler
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
        """interface just useful to locate field on dexterity types
        """
        # https://github.com/plone/plone.app.imaging/blob/ggozad-cropping/src/
        # plone/app/imaging/cropping.py

        field = self.context.getField(fieldname)
        handler = IImageScaleHandler(field)

        # TODO this is archetype only
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

        sizes = field.getAvailableSizes(self.context)
        w, h = sizes[scale]
        data = handler.createScale(self.context, scale, w, h,
                                   data=cropped_image_file.read())

        # store scale for classic <fieldname>_<scale> traversing
        handler.storeScale(self.context, scale, **data)

        # call plone.scale.storage.scale method in order to
        # provide saved scale for plone.app.imaging @@images view
        def crop_factory(fieldname, direction='keep', **parameters):
            blob = Blob()
            result = blob.open('w')
            _, image_format, dimensions = scaleImage(data['data'],
                result=result, **parameters)
            result.close()
            return blob, image_format, dimensions

        # call storage with actual time in milliseconds
        # this always invalidates old scales
        storage = AnnotationStorage(self.context,
            self.now_millis)
        storage.scale(factory=crop_factory, fieldname=fieldname,
            width=w, height=h)

        # store crop information in annotations
        self._store(fieldname, scale, box)

    @property
    def _storage(self):
        return IAnnotations(self.context).setdefault(PAI_STORAGE_KEY,
            PersistentDict())

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
