# -*- coding: utf-8 -*-
from .dx import IImageCroppingDX


class IImageCroppingBehavior(IImageCroppingDX):
    """
    Dumb marker behavior to enable imagecropping as a behavior on your own
    content types.
    """
