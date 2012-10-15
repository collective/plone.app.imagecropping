from Products.Five.browser import BrowserView
from plone.app.imaging.interfaces import IImageScaleHandler
from cStringIO import StringIO
import PIL.Image
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from plone.app.imaging.utils import getAllowedSizes

from plone.app.imagecropping.interfaces import IImageCroppingUtils


class CroppingView(BrowserView):

    def __call__(self, **kw):
        rq = self.request
        box = (rq['x1'],rq['y1'],rq['x2'],rq['y2'])

        self._crop(rq['fieldname'], rq['scale'], box)

        return "worked (xxx we might give some decent feedback to the frontend here)"

    def _crop(self, fieldname, scale, box, interface=None):
        """interface just useful to locate field on dexterity types
        """
        # https://github.com/plone/plone.app.imaging/blob/ggozad-cropping/src/plone/app/imaging/cropping.py

        croputils = IImageCroppingUtils(self.context)
        field = croputils.get_image_field(fieldname, interface)
        handler = IImageScaleHandler(field)
        data = croputils.get_image_data(fieldname, interface)

        original_file=StringIO(data)
        image = PIL.Image.open(original_file)
        image = image.crop(box)

        image_file = StringIO()
        #xxx use settings of original image (see archtetypes.clippingimage)
        image.save(image_file, 'PNG', quality=88)
        image_file.seek(0)
        sizes = getAllowedSizes()
        w, h = sizes[scale]
        data = handler.createScale(self.context, scale, w, h,
                                   data=image_file.read())
        handler.storeScale(self.context, scale, **data)
        notify(ObjectModifiedEvent(self.context))
