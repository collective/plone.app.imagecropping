from Products.Five.browser import BrowserView
from plone.app.imaging.interfaces import IImageScaleHandler
from Acquisition import aq_base
from cStringIO import StringIO
from OFS.Image import Pdata
import PIL.Image
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

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

        field = self.context.getField(fieldname)
        handler = IImageScaleHandler(field)

        # TODO this is archetype only
        value = field.get(self.context)
        data = getattr(aq_base(value), 'data', value)
        if isinstance(data, Pdata):
            data = str(data)

        original_file=StringIO(data)
        image = PIL.Image.open(original_file)
        image = image.crop(box)

        image_file = StringIO()
        #xxx use settings of original image (see archtetypes.clippingimage)
        image.save(image_file, 'PNG', quality=88)
        image_file.seek(0)
        sizes = field.getAvailableSizes(self.context)
        w, h = sizes[scale]
        data = handler.createScale(self.context, scale, w, h,
                                   data=image_file.read())
        handler.storeScale(self.context, scale, **data)
        notify(ObjectModifiedEvent(self.context))
