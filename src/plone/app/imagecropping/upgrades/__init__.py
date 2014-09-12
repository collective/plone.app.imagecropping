# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getToolByName


PROFILE_ID = 'profile-plone.app.imagecropping:default'


def _cookResources(context):
    jstool = getToolByName(context, 'portal_javascripts')
    jstool.cookResources()
    csstool = getToolByName(context, 'portal_css')
    csstool.cookResources()


def to_0004(context):
    """search for iimagecropping interface in catalog and reindex those objects
    so they implment our new interfaces
    """
    iface = 'plone.app.imagecropping.interfaces.IImageCropping'
    cat = getToolByName(context, 'portal_catalog')
    brains = cat(object_provides=iface)

    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=['object_provides'])
