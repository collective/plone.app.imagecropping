from zope.annotation.interfaces import IAnnotations

from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling

import pkg_resources
from distutils.version import LooseVersion

class ScalingOverrides(object):

    _rescale = True

    def modified(self):
        if self._rescale:
            return super(ImageScaling, self).modified()
        else:
            return 1

    def need_rescale(self, fieldname, scale):
        cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
        if cropped and '%s_%s' % (fieldname, scale) in cropped:
            self._rescale = False
        else:
            self._rescale = True



class ImageScaling(ScalingOverrides, BaseImageScaling):

    def scale(self,
              fieldname=None,
              scale=None,
              height=None,
              width=None,
              **parameters):
        self.need_rescale(fieldname, scale)
        return super(ImageScaling, self).scale(fieldname, scale, height, width, **parameters)

try:
    from plone.namedfile.scaling import ImageScaling as NFImageScaling

    from plone.namedfile.interfaces import IImageScaleTraversable
    from plone.app.imagecropping.interfaces import IImageCropping

    plone_namedfile_version = pkg_resources.get_distribution('plone.namedfile').version

    class IImageCroppingScale(IImageScaleTraversable, IImageCropping):
        pass

    class NamedfileImageScaling(ScalingOverrides, NFImageScaling):
        """ Override plone.namedfile scaling view

            This view checks, if image crops are available and
            prevents rescaling in this case.
        """

        if LooseVersion(plone_namedfile_version) >= LooseVersion('2.0.1'):
            def scale(self,
                  fieldname=None,
                  scale=None,
                  height=None,
                  width=None,
                  direction='thumbnail',
                  **parameters):
                self.need_rescale(fieldname, scale)
                return super(NamedfileImageScaling, self).scale(
                        fieldname, scale, height, width, direction, **parameters)
        else:
            def scale(self,
                  fieldname=None,
                  scale=None,
                  height=None,
                  width=None,
                  **parameters):
                self.need_rescale(fieldname, scale)
                return super(NamedfileImageScaling, self).scale(
                        fieldname, scale, height, width, **parameters)


except ImportError:
    pass
