# -*- coding: utf-8 -*-
from plone.app.imagecropping import PRODUCT_NAME
from plone.app.imagecropping.browser.settings import ISettings
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import getToolByName
from zope.component import queryUtility

import logging


logger = logging.getLogger(__name__)

PROFILE_ID = 'profile-{0:s}:default'.format(PRODUCT_NAME)


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


def migrate0002to0003(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ISettings, check=False)
    if not hasattr(settings, 'constrain_cropping'):
        settings.constrain_cropping = False
    if not hasattr(settings, 'cropping_for'):
        settings.cropping_for = []
    if not hasattr(settings, 'default_cropping_for'):
        settings.default_cropping_for = []
    logger.info('Registry cleanup operation performed')
    logger.info('Migrated to profile version 0003')


def migrate2000to2001(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ISettings, check=False)
    if not hasattr(settings, 'constrain_cropping'):
        settings.constrain_cropping = False
    if not hasattr(settings, 'cropping_for'):
        settings.cropping_for = []
    if not hasattr(settings, 'default_cropping_for'):
        settings.default_cropping_for = []
    logger.info('Registry cleanup operation performed')
    logger.info('Migrated to profile version 0003')


def migrate2001to2002(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'actions')
    logger.info('Migrated to profile version 2002')
