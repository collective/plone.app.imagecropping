# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.events import CroppingInfoChangedEvent
from plone.app.imagecropping.events import CroppingInfoRemovedEvent
from plone.scale.storage import AnnotationStorage
from z3c.caching.purge import Purge
from zope.annotation.interfaces import IAnnotations
from zope.event import notify

import time


class Storage(object):

    def __init__(self, context):
        self.context = context

    def _key(self, fieldname, scale):
        return '{0:s}_{1:s}'.format(fieldname, scale)

    def _invalidate_scale(self, fieldname, scale):
        # Call storage with actual time in milliseconds.
        # This always invalidates old scales
        scale_storage = AnnotationStorage(
            self.context,
            int(time.time())
        )
        # holzhammermethode
        uids = list(scale_storage.keys())
        for uid in uids:
            del scale_storage[uid]

    def remove(self, fieldname, scale, surpress_event=False):
        # remove info from annotation
        key = self._key(fieldname, scale)
        if key in list(self._storage.keys()):
            del self._storage[key]
        self._invalidate_scale(fieldname, scale)
        if not surpress_event:
            notify(CroppingInfoRemovedEvent(self.context))
            notify(Purge(self.context))

    @property
    def _storage(self):
        return IAnnotations(
            self.context
        ).setdefault(
            PAI_STORAGE_KEY,
            PersistentDict()
        )

    def store(self, fieldname, scale, box):
        self.remove(fieldname, scale, surpress_event=True)
        key = self._key(fieldname, scale)
        self._storage[key] = box
        notify(CroppingInfoChangedEvent(self.context))

    def read(self, fieldname, scale):
        key = self._key(fieldname, scale)
        return self._storage.get(key)
