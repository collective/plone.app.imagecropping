from zope.annotation.interfaces import IAnnotations

from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling


class ImageScaling(BaseImageScaling):

    _rescale = True

    def modified(self):
        if self._rescale:
            return super(ImageScaling, self).modified()
        else:
            return 1
    
    def scale(self,
              fieldname=None,
              scale=None,
              height=None,
              width=None,
              **parameters):
        cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
        if cropped and '%s_%s' % (fieldname, scale) in cropped:
            self._rescale = False
        else:
            self._rescale = True
        return super(ImageScaling, self).scale(fieldname, scale, height, width, **parameters)


try:
    from plone.namedfile.scaling import ImageScaling as NFImageScaling

    from plone.namedfile.interfaces import IImageScaleTraversable
    from plone.app.imagecropping.interfaces import IImageCropping

    class IImageCroppingScale(IImageScaleTraversable, IImageCropping):
        pass

    class NamedfileImageScaling(NFImageScaling):

	_rescale = True

	def modified(self):
	    if self._rescale:
		return super(NamedfileImageScaling, self).modified()
	    else:
		return 1

	def scale(self,
		  fieldname=None,
		  scale=None,
		  height=None,
		  width=None,
                  direction='thumbnail',
		  **parameters):
	    cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
	    if cropped and '%s_%s' % (fieldname, scale) in cropped:
		self._rescale = False
	    else:
		self._rescale = True
	    return super(NamedfileImageScaling, self).scale(
                fieldname, scale, height, width, direction, **parameters)

except ImportError:
    pass
