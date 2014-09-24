# -*- coding: utf-8 -*-
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imaging.utils import getAllowedSizes
from plone.behavior.interfaces import IBehaviorAssignable
from plone.namedfile.interfaces import IImage
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from zope.component import adapter
from zope.interface import implementer
from zope.schema import getFieldsInOrder
import time


class IImageCroppingDX(IImageScaleTraversable, IImageCroppingMarker):
    """Image cropping support marker interface for NamedFile/DX types
    """


def _millis():
    return int(time.time() * 1000)


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
        sizes = getAllowedSizes()
        w, h = sizes[scale]

        def crop_factory(fieldname, **parameters):
            result = scaleImage(image_file.read(), **parameters)
            if result is not None:
                data, format, dimensions = result
                mimetype = 'image/{0:s}'.format(format.lower())
                field = self.get_image_field(fieldname)
                value = field.__class__(
                    data,
                    contentType=mimetype,
                    filename=field.filename
                )
                value.fieldname = fieldname
                return value, format, dimensions

        # call storage with actual time in milliseconds
        # this always invalidates old scales
        storage = AnnotationStorage(self.context, _millis)

        # We need to pass direction='thumbnail' since this is the default
        # used by plone.namedfile.scaling, also for retrieval of scales.
        # Otherwise the key under which the scaled and cropped image is
        # saved in plone.scale.storage.AnnotationStorage will not match the
        # key used for retrieval (= the cropped scaled image will not be
        # found)
        storage.scale(
            factory=crop_factory,
            direction='thumbnail',
            fieldname=fieldname,
            width=w,
            height=h,
        )
