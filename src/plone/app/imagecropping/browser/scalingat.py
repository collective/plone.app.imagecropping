# -*- coding: utf-8 -*-
from .scaling import ScalingOverrides
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling
from ZODB.blob import Blob


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

    def _wrap_image(self, data, fmt='PNG', fieldname=None):
        blob = Blob()
        result = blob.open('w')
        result.write(data)
        result.close()
        return blob

    def scale(self, fieldname=None, scale=None, height=None, width=None,
              **parameters):
        self._scale_name = scale
        self._need_rescale(fieldname, scale)
        # if direction is 'down' and we have a cropped scale
        # deliver it instead of standard 'down' scale
        p_dir = parameters.get('direction', '')
        if p_dir == 'down' and not self._allow_rescale:
            del parameters['direction']
        return super(ImageScalingAT, self).scale(
            fieldname, scale, height, width, **parameters)
