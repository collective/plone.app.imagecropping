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

HAS_DEXTERITY = False
try:
    from plone.namedfile.interfaces import IImageScaleTraversable
    from zope.app.file.interfaces import IImage
    HAS_DEXTERITY = True
except:
    pass


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

        def image_fields(self):
            """ read interface
            """
            fields = []

            for field in self.context.getTypeInfo().lookupSchema():
                img_field = getattr(self.context, field, None)
                if img_field and IImage in providedBy(img_field).interfaces():
                    fields.append(img_field)

            return fields

        def get_image_field(self, fieldname, interface):
            """ read interface
            """
            return getattr(self.context, fieldname, None)

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
