# -*- coding: utf-8 -*-
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.lifecycleevent.interfaces import IObjectCopiedEvent


@adapter(IImageCroppingMarker, IObjectCopiedEvent)
def apply_crops_after_copy(context, event):
    crops = IAnnotations(event.original).get(PAI_STORAGE_KEY)
    if not crops:
        return
    croputils = IImageCroppingUtils(context)
    request = getRequest()
    cropper = getMultiAdapter((context, request), name='crop-image')
    for fieldname in croputils.image_field_names():
        for crop_key in crops:
            if crop_key.startswith(fieldname):
                scalename = crop_key[len(fieldname) + 1:]
                cropper._crop(fieldname, scalename, crops[crop_key])
