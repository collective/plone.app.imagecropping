# -*- coding: utf-8 -*-
from .scaling import ScalingOverrides
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling


class ImageScalingAT(ScalingOverrides, BaseImageScaling):

    def modified(self):
        """we overwrite the default method that would return the modification
        time of the context,
        to return a way back modification time in case the currently requested
        scale is a cropped scale. (so plone.scale does not create a new scale
        w/o cropping information
        """
        if self._allow_rescale:
            return super(ImageScalingAT, self).modified()
        else:
            return 1

    def scale(self, fieldname=None, scale=None, height=None, width=None,
              **parameters):
        self._need_rescale(fieldname, scale)
        return super(ImageScalingAT, self).scale(
            fieldname, scale, height, width, **parameters)
