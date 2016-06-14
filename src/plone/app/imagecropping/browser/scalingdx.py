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
        self._scale_name = scale
        self._need_rescale(fieldname, scale)
        # if direction is 'down' and we have a cropped scale
        # deliver it instead of standard 'down' scale
        if direction == 'down' and not self._allow_rescale:
            direction = 'thumbnail'
        return super(ImageScalingDX, self).scale(
            fieldname, scale, height, width, direction, **parameters)

    def _wrap_image(self, data, fmt='PNG', fieldname=None):
        if not fieldname:
            return
        orig_value = getattr(self.context, fieldname)
        if orig_value is None:
            return
        mimetype = 'image/%s' % fmt.lower()
        value = orig_value.__class__(
            data, contentType=mimetype, filename=orig_value.filename)
        value.fieldname = fieldname
        return value
