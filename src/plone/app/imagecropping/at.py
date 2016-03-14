# -*- coding: utf-8 -*-
from Acquisition import aq_base
from OFS.Image import Pdata
from plone.app.blob.config import blobScalesAttr
from plone.app.blob.interfaces import IBlobImageField
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.app.imaging.traverse import ImageTraverser as BaseImageTraverser
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from Products.Archetypes.interfaces.field import IImageField
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from ZODB.blob import Blob
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces import IRequest

import time


class IImageCroppingAT(IImageCroppingMarker):
    """Image cropping support marker interface for Archetypes based content
    """


def _millis():
    return int(time.time() * 1000)


@implementer(IImageCroppingUtils)
@adapter(IATContentType)
class CroppingUtilsArchetype(object):

    def __init__(self, context):
        self.context = context

    def image_fields(self):
        """ read interface
        """
        fields = []

        for field in self.context.Schema().fields():
            if (
                IBlobImageField.providedBy(field) or
                IImageField.providedBy(field) and
                field.get_size(self.context) > 0
            ):
                fields.append(field)

        return fields

    def image_field_names(self):
        """ read interface
        """
        return [field.__name__ for field in self.image_fields()]

    def get_image_field(self, fieldname):
        """ read interface
        """
        return self.context.getField(fieldname)

    def get_image_label(self, fieldname):
        field = self.get_image_field(fieldname)
        return field.widget.label

    def get_image_data(self, fieldname):
        """ read interface
        """
        field = self.get_image_field(fieldname)
        blob = field.get(self.context)
        data = getattr(aq_base(blob), 'data', blob)
        if isinstance(data, Pdata):
            data = str(data)
        return data

    def get_image_size(self, fieldname):
        """ read interface
        """
        field = self.get_image_field(fieldname)
        image_size = field.getSize(self.context)
        return image_size

    def save_cropped(self, fieldname, scale, image_file):
        """ see interface
        """
        field = self.get_image_field(fieldname)
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

        # Avoid browser cache
        # calling reindexObject updates the modified metadate too
        self.context.reindexObject()

        # call storage with actual time in milliseconds
        # this always invalidates old scales
        storage = AnnotationStorage(self.context, _millis)
        storage.scale(
            factory=crop_factory, fieldname=field.__name__, width=w, height=h)


@adapter(IImageCroppingAT, IRequest)
class ImageTraverser(BaseImageTraverser):
    """extend the standard image traverser to remove our cropping annotations
    (if present) in case the original image has been removed/replaced
    (no blobScalesAttr)
    """

    def publishTraverse(self, request, name):
        # remove scales information, if image has changed
        # We have no way of knowing if a non-blob image has changed, since we
        # don't have a time marker for when crops were generated.
        has_blobs = False
        for field in self.context.Schema().fields():
            if IBlobImageField.providedBy(field):
                has_blobs = True
                break

        if has_blobs and not hasattr(aq_base(self.context), blobScalesAttr) \
           and PAI_STORAGE_KEY in IAnnotations(self.context):
            del IAnnotations(self.context)[PAI_STORAGE_KEY]
        return super(ImageTraverser, self).publishTraverse(request, name)
