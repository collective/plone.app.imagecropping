# -*- coding: utf-8 -*-
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCopiedEvent


@adapter(IImageCroppingMarker, IObjectCopiedEvent)
def apply_crops_after_copy(context, event):
    crops = IAnnotations(event.original).get(PAI_STORAGE_KEY)

    if crops:
        IAnnotations(context).setdefault(PAI_STORAGE_KEY, crops)

    # TODO: I think we have to trigger thumb creation, right?
