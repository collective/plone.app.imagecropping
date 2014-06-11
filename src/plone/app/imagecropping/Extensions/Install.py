# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.imagecropping import PRODUCT_NAME

UNINSTALL_PROFILE = 'profile-{0:s}:uninstall'.format(PRODUCT_NAME)


def uninstall(context, reinstall):
    if not reinstall:
        setup_tool = getToolByName(context, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(UNINSTALL_PROFILE)

    # remove controlpanel
    cp_tool = context['portal_controlpanel']
    cp_tool.unregisterApplication('ImageCroppingSettings')
