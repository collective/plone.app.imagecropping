# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.app.blob.config import blobScalesAttr
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from plone.app.imaging.traverse import ImageTraverser as BaseImageTraverser
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.publisher.interfaces import IRequest
import time


class BaseUtil(object):
    """Base utility with methods for both Archetypes and dexterity
    """

    def __init__(self, context):
        self.context = context

    def now_millis(self):
        return int(time.time() * 1000)


@adapter(IImageCroppingMarker, IRequest)
class ImageTraverser(BaseImageTraverser):
    """extend the standard image traverser to remove our cropping annotations
    (if present) in case the original image has been removed/replaced
    (no blobScalesAttr)
    """

    def publishTraverse(self, request, name):
        # remove scales information, if image has changed
        if not hasattr(aq_base(self.context), blobScalesAttr) \
           and PAI_STORAGE_KEY in IAnnotations(self.context):
                del IAnnotations(self.context)[PAI_STORAGE_KEY]
        return super(ImageTraverser, self).publishTraverse(request, name)
