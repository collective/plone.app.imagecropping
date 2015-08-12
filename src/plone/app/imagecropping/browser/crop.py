# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from cStringIO import StringIO
from persistent.dict import PersistentDict
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.scale.storage import AnnotationStorage
from z3c.caching.purge import Purge
from zope.annotation.interfaces import IAnnotations
from zope.event import notify

import PIL.Image


class CroppingView(BrowserView):

    DEFAULT_FORMAT = 'PNG'

    def __call__(self, **kw):
        rq = self.request
        box = (rq['x1'], rq['y1'], rq['x2'], rq['y2'])

        self._crop(rq['fieldname'], rq['scale'], box)

        return True

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

        # Purge caches if needed
        notify(Purge(self.context))

    @property
    def _storage(self):
        return IAnnotations(self.context).setdefault(
            PAI_STORAGE_KEY, PersistentDict())

    def _store(self, fieldname, scale, box):
        self._storage['{0:s}_{1:s}'.format(fieldname, scale)] = box
        return True

    def _read(self, fieldname, scale):
        return self._storage.get('{0:s}_{1:s}'.format(fieldname, scale))

    def _remove(self, fieldname, scale):
        # remove info from annotation
        key = '{0:s}_{1:s}'.format(fieldname, scale)
        if key in self._storage.keys():
            del self._storage[key]

        # remove saved scale
        scale_storage = AnnotationStorage(self.context)
        image_scales = self.context.restrictedTraverse('@@images')
        image_scale = image_scales.scale(fieldname, scale=scale)
        del scale_storage[image_scale.uid]
