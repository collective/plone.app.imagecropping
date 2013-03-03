from Products.Five.browser import BrowserView

from cStringIO import StringIO
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.scale.storage import AnnotationStorage
from zope.annotation.interfaces import IAnnotations
import PIL.Image


class CroppingView(BrowserView):

    DEFAULT_FORMAT = 'PNG'

    def __call__(self, **kw):
        rq = self.request
        box = (rq['x1'], rq['y1'], rq['x2'], rq['y2'])

        self._crop(rq['fieldname'], rq['scale'], box)

        return True

    def _crop(self, fieldname, scale, box, interface=None):
        """switch between dexterity and Archetypes
        """
        croputils = IImageCroppingUtils(self.context)
        field = croputils.get_image_field(fieldname)
        data = croputils.get_image_data(fieldname)

        original_file = StringIO(data)
        image = PIL.Image.open(original_file)
        image_format = image.format or self.DEFAULT_FORMAT

        cropped_image = image.crop(box)
        cropped_image_file = StringIO()
        cropped_image.save(cropped_image_file, image_format, quality=100)
        cropped_image_file.seek(0)

        croputils.save_cropped(
            fieldname, field, scale, cropped_image_file, interface)

        # store crop information in annotations
        self._store(fieldname, scale, box)

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
