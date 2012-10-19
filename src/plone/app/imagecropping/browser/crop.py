from Acquisition import aq_base
from OFS.Image import Pdata
from Products.Five.browser import BrowserView
from cStringIO import StringIO
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.scale.storage import AnnotationStorage
from zope.annotation.interfaces import IAnnotations
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import PIL.Image


class CroppingView(BrowserView):

    DEFAULT_FORMAT = 'PNG'

    def __call__(self, **kw):
        rq = self.request
        box = (rq['x1'], rq['y1'], rq['x2'], rq['y2'])

        self._crop(rq['fieldname'], rq['scale'], box)

        return True

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
        image = image.crop(box)

        image_file = StringIO()

        # FIXME: try to save image in it's original format if it can be guessed
        #quality will be reduced by createScale anyway so we pass it
        #w/o reducing quality
        format = image.format or self.DEFAULT_FORMAT
        image.save(image_file, format, quality=100)

        image_file.seek(0)
        sizes = field.getAvailableSizes(self.context)
        w, h = sizes[scale]
        data = handler.createScale(self.context, scale, w, h,
                                   data=image_file.read())
        handler.storeScale(self.context, scale, **data)

        # store crop information
        self._store(fieldname, scale, box)

        notify(ObjectModifiedEvent(self.context))

    def _store(self, fieldname, scale, box):
        storage = IAnnotations(self.context).setdefault(PAI_STORAGE_KEY,
            PersistentDict())
        storage["%s-%s" % (fieldname, scale)] = box
