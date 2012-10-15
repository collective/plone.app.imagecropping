from zope.interface.interface import Interface


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

    def get_image_data(fieldname, interface):
        """Returns the image data"""

    def get_image_size(fieldname, interface):
        """Returns the original image size:

           (100, 200)
        """
