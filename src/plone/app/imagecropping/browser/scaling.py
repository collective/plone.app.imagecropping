# -*- coding: utf-8 -*-
from plone.app.imagecropping import PAI_STORAGE_KEY
from zope.annotation.interfaces import IAnnotations


class ScalingOverrides(object):

    _allow_rescale = True

    def _need_rescale(self, fieldname, scale):
        """If we've got a cropping annotation for the given fieldname
           and scale, set self._allow_rescale to False, to prevent
           plone.app.imaging traverser to overwrite our cropped scale

           since the self.modified() method does not know about the
           currently requested scale name, we need to use the _allow_rescale
           property.

           AT only! Solved for dexterity.
        """
        cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
        if cropped and '{0:s}_{1:s}'.format(fieldname, scale) in cropped:
            self._allow_rescale = False
        else:
            self._allow_rescale = True
