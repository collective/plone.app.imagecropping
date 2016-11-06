# -*- coding: utf-8 -*-
from zope.component.interfaces import IObjectEvent
from zope.interface.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPloneAppImagecroppingLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IImageCroppingMarker(Interface):
    """Generic marker interface for image cropping support.

    do not use directly, use the more special interfaces in dx or at modules
    """


class IImageCroppingUtils(Interface):
    """Methods to help the cropping editor views.
       The implementation is different for Archetype and Dexterity context.
    """

    def image_fields():
        """Returns all image fields"""

    def image_field_names():
        """Returns the names of all image fields"""

    def get_image_field(fieldname):
        """Returns the image field"""

    def get_image_label(fieldname):
        """Returns the label of the image field"""

    def get_image_data(fieldname):
        """Returns the image data"""

    def get_image_size(fieldname):
        """Returns the original image size:

           (100, 200)
        """

    def save_cropped(fieldname, scale, image_file):
        """ Save the cropped image under the name of the selected scale in
            plone.scale.storage.AnnotationStorage, so that it is available
            in plone.app.imaging @@images view

            DEPRECATED/ BBB - this is superseeded by usage of scaling factories
        """


class ICroppingInfoChangedEvent(IObjectEvent):
    """ event after cropping information has changed """


class ICroppingInfoRemovedEvent(IObjectEvent):
    """ event after cropping information has changed """


# seems unused
# class ICroppedImageScaling(IImageScaling):
#     """ marker for @@images overrides """


# class ICroppedBlobImageField(IBlobImageField):
#     """ marker for coppable blob image field adapters """
