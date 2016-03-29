# -*- coding: utf-8 -*-
from plone.app.imagecropping.browser.settings import ISettings
from plone.app.imagecropping.testing import IMAGECROPPING_INTEGRATION
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        self.qi_tool = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name='imagecropping-settings'
        )
        view = view.__of__(self.portal)
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
        self.qi_tool = self.portal['portal_quickinstaller']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISettings)

    def test_available_sections_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'large_size'))
        self.assertEqual(self.settings.large_size, u'768:768')

    def test_default_section_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'min_size'))
        self.assertEqual(self.settings.min_size, u'50:50')

    def test_records_removed_on_uninstall(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi_tool.uninstallProducts(products=['plone.app.imagecropping'])

        BASE_REGISTRY = \
            'plone.app.imagecropping.browser.settings.ISettings.{0:s}'
        records = (
            BASE_REGISTRY.format('large_size'),
            BASE_REGISTRY.format('min_size'),
        )

        for r in records:
            self.assertNotIn(r, self.registry)
