from zope.interface.interface import Interface
from plone.app.imaging.interfaces import IImageScaling
from plone.app.blob.interfaces import IBlobImageField


class IImageCropping(Interface):
    """ marker interface for image cropping support """


class IImageCroppingUtils(Interface):
    """Methods to help the cropping editor views.
       The implementation is different for Archetype and Dexterity context.
    """

    def image_fields():
        """Returns all image fields and additional information:

           {'fieldname1': {"title" :  "super image"
                           'preview_url': 'http:..',
                           'interface': interface.Inteface,
                           },
            }
        """

    def get_image_field(fieldname, interface):
        """Returns the image field"""

    def get_image_data(fieldname, interface):
        """Returns the image data"""

    def get_image_size(fieldname, interface):
        """Returns the original image size:

           (100, 200)
        """


class ICroppedImageScaling(IImageScaling):
    """ marker for @@images overrides """


class ICroppedBlobImageField(IBlobImageField):
    """ marker for coppable blob image field adapters """
