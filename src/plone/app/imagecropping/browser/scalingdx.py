# -*- coding: utf-8 -*-
from .scaling import ScalingOverrides
from plone.namedfile.scaling import ImageScaling as NFImageScaling


class ImageScalingDX(ScalingOverrides, NFImageScaling):
    """ Override plone.namedfile scaling view

        This view checks, if image crops are available and
        prevents rescaling in this case.
    """

    def modified(self):
        """We overwrite the default method that would return the
           modification time of the context, to return a way back
           modification time in case the currently requested scale
           is a cropped scale. (so plone.scale does not create a
           new scale w/o cropping information.
        """
        if self._allow_rescale:
            return super(ImageScalingDX, self).modified()
        else:
            return 1

    def scale(self, fieldname=None, scale=None, height=None, width=None,
              direction='thumbnail', **parameters):
        self._need_rescale(fieldname, scale)
        # XXX: introduce a new direction 'autodown'
        # this returns the cropped scale if available, otherwise the
        # normal 'down'-scaled scale
        if direction == 'autodown':
            direction = self._allow_rescale and 'down' or 'thumbnail'
        return super(ImageScalingDX, self).scale(
            fieldname, scale, height, width, direction, **parameters)
