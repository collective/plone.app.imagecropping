# -*- coding: utf-8 -*-
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling
from zope.annotation.interfaces import IAnnotations


class ScalingOverrides(object):

    _allow_rescale = True

    def _need_rescale(self, fieldname, scale):
        """If we've got a cropping annotation for the given fieldname
           and scale, set self._rescale to False, to prevent
           plone.app.imaging traverser to overwrite our cropped scale

           since the self.modified() method does not know about the
           currently requested scale name, we need to use the _rescale
           property
        """
        cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
        if cropped and '%s_%s' % (fieldname, scale) in cropped:
            self._allow_rescale = False
        else:
            self._allow_rescale = True


class ImageScaling(ScalingOverrides, BaseImageScaling):

    def modified(self):
        """we overwrite the default method that would return the modification
        time of the context,
        to return a way back modification time in case the currently requested
        scale is a cropped scale. (so plone.scale does not create a new scale
        w/o cropping information
        """
        if self._allow_rescale:
            return super(ImageScaling, self).modified()
        else:
            return 1

    def scale(self, fieldname=None, scale=None, height=None, width=None,
              **parameters):
        self._need_rescale(fieldname, scale)
        return super(ImageScaling, self).scale(
            fieldname, scale, height, width, **parameters)

try:
    from plone.app.imagecropping.interfaces import IImageCropping
    from plone.namedfile.interfaces import IImageScaleTraversable
    from plone.namedfile.scaling import ImageScaling as NFImageScaling

    class IImageCroppingScale(IImageScaleTraversable, IImageCropping):
        pass

    class NamedfileImageScaling(ScalingOverrides, NFImageScaling):
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
                return super(NamedfileImageScaling, self).modified()
            else:
                return 1

        def scale(self, fieldname=None, scale=None, height=None, width=None,
                  direction='thumbnail', **parameters):
            self._need_rescale(fieldname, scale)
            return super(NamedfileImageScaling, self).scale(
                fieldname, scale, height, width, direction, **parameters)

except ImportError:
    pass
