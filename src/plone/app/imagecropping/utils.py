# -*- coding: utf-8 -*-
from Acquisition import aq_base
from OFS.Image import Pdata
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.Archetypes.interfaces.field import IImageField
from plone.app.blob.interfaces import IBlobImageField
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from zope.component import adapts
from zope.interface import implements
from zope.interface.declarations import providedBy

from plone.app.imagecropping import HAS_DEXTERITY
if HAS_DEXTERITY:
    from plone.namedfile.interfaces import IImageScaleTraversable
    from plone.namedfile.interfaces import IImage


class CroppingUtilsArchetype(object):
    """TODO"""

    implements(IImageCroppingUtils)
    adapts(IATContentType)

    def __init__(self, context):
        self.context = context

    def image_fields(self):
        """ read interface
        """
        fields = []

        for field in self.context.Schema().fields():
            if IBlobImageField in providedBy(field).interfaces() or \
               IImageField in providedBy(field).interfaces() and \
               field.get_size(self.context) > 0:
                fields.append(field)

        return fields

    def image_field_names(self):
        """ read interface
        """
        return [field.__name__ for field in self.image_fields()]

    def get_image_field(self, fieldname, interface):
        """ read interface
        """
        return self.context.getField(fieldname)

    def get_image_data(self, fieldname, interface):
        """ read interface
        """
        field = self.get_image_field(fieldname, interface)
        blob = field.get(self.context)
        data = getattr(aq_base(blob), 'data', blob)
        if isinstance(data, Pdata):
            data = str(data)
        return data

    def get_image_size(self, fieldname, interface):
        """ read interface
        """
        field = self.get_image_field(fieldname, interface)
        image_size = field.getSize(self.context)
        return image_size


if HAS_DEXTERITY:
    class CroppingUtilsDexterity(object):
        """TODO"""

        implements(IImageCroppingUtils)
        adapts(IImageScaleTraversable)

        def __init__(self, context):
            self.context = context

        def _image_field_info(self):
            fields = []

            for fieldname in self.context.getTypeInfo().lookupSchema():
                img_field = getattr(self.context, fieldname, None)
                if img_field and IImage.providedBy(img_field):
                    fields.append((fieldname, img_field))

            return fields

        def image_fields(self):
            """ read interface
            """
            return [info[1] for info in self._image_field_info()]

        def image_field_names(self):
            """ read interface
            """
            return [info[0] for info in self._image_field_info()]

        def get_image_field(self, fieldname, interface):
            """ read interface
            """
            return getattr(self.context, fieldname, None)

        def get_image_data(self, fieldname, interface):
            """ read interface
            """
            field = self.get_image_field(fieldname, interface)
            return field.data

        def get_image_size(self, fieldname, interface):
            """ read interface
            """
            field = self.get_image_field(fieldname, interface)
            image_size = field.getImageSize()
            return image_size
