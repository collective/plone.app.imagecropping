# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import implements

from Products.ATContentTypes.interfaces.interfaces import IATContentType
from plone.app.imagecropping.interfaces import IImageCroppingUtils


class CroppingUtilsArchetype(object):
    """TODO"""

    implements(IImageCroppingUtils)
    adapts(IATContentType)

    def __init__(self, context):
        self.context = context


    def image_fields():
        """ read interface
        """

    def get_image_data(fieldname, interface):
        """ read interface
        """

    def get_image_size(fieldname, interface):
        """ read interface
        """

