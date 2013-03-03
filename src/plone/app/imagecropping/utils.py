# -*- coding: utf-8 -*-
from Acquisition import aq_base
from OFS.Image import Pdata
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.Archetypes.interfaces.field import IImageField
from ZODB.blob import Blob
from plone.app.blob.interfaces import IBlobImageField
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.app.imaging.utils import getAllowedSizes
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from zope.component import adapts
from zope.interface import implements
from zope.interface.declarations import providedBy

import time

from plone.app.imagecropping import HAS_DEXTERITY
if HAS_DEXTERITY:
    from plone.namedfile.interfaces import IImage
    from plone.namedfile.interfaces import IImageScaleTraversable


class BaseUtil(object):
    """Base utility with methods for both Archetypes and dexterity
    """

    def __init__(self, context):
        self.context = context

    def now_millis(self):
        return int(time.time() * 1000)


class CroppingUtilsArchetype(BaseUtil):
    """TODO"""

    implements(IImageCroppingUtils)
    adapts(IATContentType)

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

    def get_image_field(self, fieldname, interface=None):
        """ read interface
        """
        return self.context.getField(fieldname)

    def get_image_data(self, fieldname, interface=None):
        """ read interface
        """
        field = self.get_image_field(fieldname, interface)
        blob = field.get(self.context)
        data = getattr(aq_base(blob), 'data', blob)
        if isinstance(data, Pdata):
            data = str(data)
        return data

    def get_image_size(self, fieldname, interface=None):
        """ read interface
        """
        field = self.get_image_field(fieldname, interface)
        image_size = field.getSize(self.context)
        return image_size

    def save_cropped(
            self, fieldname, field, scale, image_file, interface=None):
        """ see interface
        """
        handler = IImageScaleHandler(field)
        sizes = field.getAvailableSizes(self.context)
        w, h = sizes[scale]
        data = handler.createScale(
            self.context, scale, w, h, data=image_file.read())

        # store scale for classic <fieldname>_<scale> traversing
        handler.storeScale(self.context, scale, **data)

        # call plone.scale.storage.scale method in order to
        # provide saved scale for plone.app.imaging @@images view
        def crop_factory(fieldname, direction='keep', **parameters):
            blob = Blob()
            result = blob.open('w')
            _, image_format, dimensions = scaleImage(
                data['data'], result=result, **parameters)
            result.close()
            return blob, image_format, dimensions

        # call storage with actual time in milliseconds
        # this always invalidates old scales
        storage = AnnotationStorage(self.context, self.now_millis)
        storage.scale(
            factory=crop_factory, fieldname=field.__name__, width=w, height=h)

if HAS_DEXTERITY:
    class CroppingUtilsDexterity(BaseUtil):
        """TODO"""

        implements(IImageCroppingUtils)
        adapts(IImageScaleTraversable)

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

        def get_image_field(self, fieldname, interface=None):
            """ read interface
            """
            return getattr(self.context, fieldname, None)

        def get_image_data(self, fieldname, interface=None):
            """ read interface
            """
            field = self.get_image_field(fieldname, interface)
            return field.data

        def get_image_size(self, fieldname, interface=None):
            """ read interface
            """
            field = self.get_image_field(fieldname, interface)
            image_size = field.getImageSize()
            return image_size

        def save_cropped(
                self, fieldname, field, scale, image_file, interface=None):
            """ see interface
            """
            sizes = getAllowedSizes()
            w, h = sizes[scale]

            def crop_factory(fieldname, **parameters):
                result = scaleImage(image_file.read(), **parameters)
                if result is not None:
                    data, format, dimensions = result
                    mimetype = 'image/%s' % format.lower()
                    value = field.__class__(
                        data,
                        contentType=mimetype,
                        filename=field.filename
                    )
                    value.fieldname = fieldname
                    return value, format, dimensions

            # call storage with actual time in milliseconds
            # this always invalidates old scales
            storage = AnnotationStorage(self.context, self.now_millis)

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
