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

    # this consumes a lot of memory if we have too many objects to
    # update; we better use a generator to reduce memory usage and
    # avoid restarts on instances running with supervisor's memmon
    results = (b.getObject() for b in cat(object_provides=iface))
    for obj in results:
        obj.reindexObject(idxs=['object_provides'])
