from Acquisition import aq_base
from DateTime import DateTime
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.events import CroppingInfoChangedEvent
from plone.app.imagecropping.events import CroppingInfoRemovedEvent
from plone.scale.storage import AnnotationStorage
from z3c.caching.purge import Purge
from zope.annotation.interfaces import IAnnotations
from zope.event import notify

import time


class Storage:
    def __init__(self, context):
        self.context = context

    def _key(self, fieldname, scale):
        return f"{fieldname:s}_{scale:s}"

    def _invalidate_scale(self, fieldname, scale):
        # Call storage with actual time in milliseconds.
        # This always invalidates old scales
        scale_storage = AnnotationStorage(self.context, int(time.time()))
        scale_storage.clear()

    def remove(self, fieldname, scale, supress_event=False):
        # remove info from annotation
        key = self._key(fieldname, scale)
        if key in list(self._storage.keys()):
            del self._storage[key]
        self._invalidate_scale(fieldname, scale)
        if not supress_event:
            notify(CroppingInfoRemovedEvent(self.context))
            notify(Purge(self.context))
            self.context.reindexObject()

    @property
    def _storage(self):
        return IAnnotations(self.context).setdefault(PAI_STORAGE_KEY, PersistentDict())

    def store(self, fieldname, scale, box):
        self.remove(fieldname, scale, supress_event=True)
        key = self._key(fieldname, scale)
        self._storage[key] = box

        context = aq_base(self.context)
        field = getattr(context, fieldname, None)
        if field is not None:
            field._modified = DateTime().millis()  # Force a new hash key

        notify(CroppingInfoChangedEvent(self.context))
        notify(Purge(self.context))

    def read(self, fieldname, scale):
        if not scale:
            return
        key = self._key(fieldname, scale)
        return self._storage.get(key)
