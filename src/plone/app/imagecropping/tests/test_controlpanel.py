# -*- coding: utf-8 -*-
from plone import api
from plone.app.imagecropping.browser.settings import ISettings
from plone.app.imagecropping.testing import IMAGECROPPING_INTEGRATION
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    # BBB for Plone 5.0 and lower.
    get_installer = None


class ControlPanelTestCase(unittest.TestCase):

    layer = IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        if get_installer is None:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        else:
            self.installer = get_installer(self.portal)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name='imagecropping-settings'
        )
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            '@@imagecropping-settings'
        )


class RegistryTestCase(unittest.TestCase):

    layer = IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer is None:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        else:
            self.installer = get_installer(self.portal)
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISettings)

    def test_records_removed_on_uninstall(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        if get_installer is None:
            self.installer.uninstallProducts(
                products=['plone.app.imagecropping'])
        else:
            self.installer.uninstall_product('plone.app.imagecropping')

        BASE_REGISTRY = \
            'plone.app.imagecropping.browser.settings.ISettings.{0:s}'
        records = (
            BASE_REGISTRY.format('large_size'),
            BASE_REGISTRY.format('min_size'),
        )

        for r in records:
            self.assertNotIn(r, self.registry)
