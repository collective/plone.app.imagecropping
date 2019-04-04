# -*- coding: utf-8 -*-
from io import BytesIO
from plone.app.imagecropping.browser.settings import ISettings
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imagecropping.storage import Storage
from plone.behavior.interfaces import IBehaviorAssignable
from plone.namedfile.interfaces import IImage
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.scaling import DefaultImageScalingFactory
from plone.registry.interfaces import IRegistry
from zope.component import adapter
from zope.component._api import getUtility
from zope.interface import implementer
from zope.schema import getFieldsInOrder

import PIL


class IImageCroppingDX(IImageScaleTraversable, IImageCroppingMarker):
    """Image cropping support marker interface for NamedFile/DX types
    """


@adapter(IImageCroppingDX)  # this would work almost also on AT!
class CroppingImageScalingFactory(DefaultImageScalingFactory):

    def _crop(self, data, box, default_format='PNG'):
        """crop data (image as open file) to box
        """
        image = PIL.Image.open(data)
        image_format = image.format or default_format
        cropped_image = image.crop(box)
        cropped_image_file = BytesIO()
        cropped_image.save(cropped_image_file, image_format, quality=100)
        cropped_image_file.seek(0)
        return cropped_image_file

    def create_scale(self, data, direction, height, width, **parameters):
        if self.box:
            # do crop stuff first
            data = self._crop(data, self.box)
        return super(CroppingImageScalingFactory, self).create_scale(
            data,
            direction,
            height,
            width,
            **parameters
        )

    def __call__(
        self,
        fieldname=None,
        direction='thumbnail',
        height=None,
        width=None,
        scale=None,
        **parameters
    ):
        storage = Storage(self.context)
        self.box = storage.read(fieldname, scale)
        if self.box:
            direction = 'down'
        else:
            registry = getUtility(IRegistry)
            settings = registry.forInterface(ISettings)
            if scale in settings.cropping_for:
                direction = 'down'
        return super(CroppingImageScalingFactory, self).__call__(
            fieldname=fieldname,
            direction=direction,
            height=height,
            width=width,
            scale=scale,
            **parameters
        )


@implementer(IImageCroppingUtils)
@adapter(IImageScaleTraversable)
class CroppingUtilsDexterity(object):
    """Dexterity variant of scaling adapter
    """

    def __init__(self, context):
        self.context = context

    def _all_fields(self):
        type_info = self.context.getTypeInfo()
        if type_info is None:
            return
        schema = type_info.lookupSchema()
        for field in getFieldsInOrder(schema):
            yield field
        behavior_assignable = IBehaviorAssignable(self.context)
        if behavior_assignable:
            for behavior in behavior_assignable.enumerateBehaviors():
                for field in getFieldsInOrder(behavior.interface):
                    yield field

    def _image_field_values(self):
        for fieldname, field in self._all_fields():
            value = getattr(self.context, fieldname, None)
            if value and IImage.providedBy(value):
                yield (fieldname, value)

    def image_fields(self):
        """ read interface
        """
        return [info[1] for info in self._image_field_values()]

    def image_field_names(self):
        """ read interface
        """
        return [info[0] for info in self._image_field_values()]

    def get_image_field(self, fieldname):
        """ read interface
        """
        return getattr(self.context, fieldname, None)

    def get_image_label(self, fieldname):
        for name, field in self._all_fields():
            if name == fieldname:
                return field.title
        return fieldname

    def get_image_data(self, fieldname):
        """ read interface
        """
        field = self.get_image_field(fieldname)
        return field.data

    def get_image_size(self, fieldname):
        """ read interface
        """
        field = self.get_image_field(fieldname)
        image_size = field.getImageSize()
        return image_size

    def save_cropped(self, fieldname, scale, image_file):
        """ see interface
        """
        # BBB - this is superseeded by usage of scaling factories
        pass
