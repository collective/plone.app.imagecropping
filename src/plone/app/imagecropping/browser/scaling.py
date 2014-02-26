from zope.annotation.interfaces import IAnnotations

from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling


class ImageScaling(BaseImageScaling):

    def modified(self):
        cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
        if not cropped:
            return super(ImageScaling, self).modified()
        else:
            return 1


# XXX need this for plone.namedfile and NEWSItem too
