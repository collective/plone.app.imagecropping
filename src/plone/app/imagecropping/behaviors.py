# -*- coding: utf-8 -*-
from plone.app.imagecropping.dx import IImageCroppingDX


class IImageCroppingBehavior(IImageCroppingDX):
    """
    Dumb marker behavior to enable imagecropping as a behavior on your own
    content types.
    """
