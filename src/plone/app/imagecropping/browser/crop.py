# -*- coding: utf-8 -*-
from cStringIO import StringIO
from persistent.dict import PersistentDict
from plone import api
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.events import CroppingInfoChangedEvent
from plone.app.imagecropping.events import CroppingInfoRemovedEvent
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.scale.storage import AnnotationStorage
from Products.Five.browser import BrowserView
from z3c.caching.purge import Purge
from zope.annotation.interfaces import IAnnotations
from zope.event import notify

import logging
import PIL.Image


logger = logging.getLogger(__name__)


class CroppingView(BrowserView):

    DEFAULT_FORMAT = 'PNG'

    def __call__(self, **kw):
        form = self.request.form
        fieldname = form['fieldname']
        scale_id = form['scale']
        if 'remove' in form:
            self._remove(fieldname, scale_id)
            return 'OK'

        box = (
            int(round(float(form['x']))),
            int(round(float(form['y']))),
            int(round(float(form['x']) + float(form['width']))),
            int(round(float(form['y']) + float(form['height']))),
        )
        self._crop(form['fieldname'], form['scale'], box)
        return 'OK'

    def _crop(self, fieldname, scale, box):
        """switch between dexterity and Archetypes
        """
        croputils = IImageCroppingUtils(self.context)
        data = croputils.get_image_data(fieldname)

        original_file = StringIO(data)
        image = PIL.Image.open(original_file)
        image_format = image.format or self.DEFAULT_FORMAT

        cropped_image = image.crop(box)
        cropped_image_file = StringIO()
        cropped_image.save(cropped_image_file, image_format, quality=100)
        cropped_image_file.seek(0)

        croputils.save_cropped(fieldname, scale, cropped_image_file)

        # store crop information in annotations
        self._store(fieldname, scale, box)

        notify(CroppingInfoChangedEvent(self.context))
        # Purge caches if needed
        notify(Purge(self.context))

    def _key(self, fieldname, scale):
        return '{0:s}_{1:s}'.format(fieldname, scale)

    def _remove(self, fieldname, scale):
        # remove info from annotation
        key = self._key(fieldname, scale)
        if key in self._storage.keys():
            del self._storage[key]

        # remove saved scale
        scale_storage = AnnotationStorage(self.context)
        image_scales = api.content.get_view(
            'images',
            self.context,
            self.request
        )
        image_scale = image_scales.scale(fieldname, scale=scale)
        del scale_storage[image_scale.uid]

        notify(CroppingInfoRemovedEvent(self.context))
        # Purge caches if needed
        notify(Purge(self.context))

    @property
    def _storage(self):
        return IAnnotations(
            self.context
        ).setdefault(
            PAI_STORAGE_KEY,
            PersistentDict()
        )

    def _store(self, fieldname, scale, box):
        key = self._key(fieldname, scale)
        self._storage[key] = box

    def _read(self, fieldname, scale):
        key = self._key(fieldname, scale)
        return self._storage.get(key)
