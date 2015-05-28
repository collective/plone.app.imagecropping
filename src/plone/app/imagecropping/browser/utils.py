from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingMarker
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from zope.annotation.interfaces import IAnnotations

import logging

logger = logging.getLogger('plone.app.imagecropping')


class RecreateCroppedScales(BrowserView):
    """Sometimes it can happen, that the cropped scale(s) of an imagefield
    get lost when editing it's content item (see #21 and #54)
    
    This utility view searches for all items implementing IImageCroppingMarker
    and recreates cropped versions for all scales that have been manually
    cropped (having a `plone.app.imagecropping` annotation)
    """

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        croppables = (brain.getObject() for brain in catalog(object_provides=IImageCroppingMarker.__identifier__))
        with_cropping_info = 0
        total = 0
        total_scales = 0
        for obj in croppables:
            total += 1

            infos = IAnnotations(obj).get(PAI_STORAGE_KEY, None)
            if infos is None:
                continue
            with_cropping_info += 1
            cropview = obj.restrictedTraverse('@@crop-image')
            utils = IImageCroppingUtils(obj)
            fieldnames = utils.image_field_names()
            for field_scale, box in infos.iteritems():
                for fieldname in fieldnames:
                    if field_scale.startswith(fieldname):
                        scalename = field_scale.replace(fieldname + '_', '')
                        logger.info("recreate {0} for {1}".format(
                            field_scale, '/'.join(obj.getPhysicalPath())))
                        cropview._crop(fieldname, scalename, box)
                        total_scales += 1


        msg = "found {0} croppable objects ({1} with cropping info) and re-created {2} scales".format(
            total, with_cropping_info, total_scales)

        logger.warn(msg)

        return msg
