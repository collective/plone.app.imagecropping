# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.imagecropping.testing import IMAGECROPPING_FUNCTIONAL

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    # BBB for Plone 5.0 and lower.
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that plone.app.imagecropping is properly installed."""

    layer = IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer is None:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        else:
            self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if plone.app.imagecropping is installed."""
        if get_installer is None:
            is_installed = self.installer.isProductInstalled(
                'plone.app.imagecropping')
        else:
            is_installed = self.installer.is_product_installed(
                'plone.app.imagecropping')
        self.assertTrue(is_installed)

    def test_browserlayer(self):
        """Test that IPloneAppImagecroppingLayer is registered."""
        from plone.app.imagecropping.interfaces import (
            IPloneAppImagecroppingLayer)
        from plone.browserlayer import utils
        self.assertIn(IPloneAppImagecroppingLayer, utils.registered_layers())

    def test_controlpanel(self):
        actions = [
            a.getAction(self)['id']
            for a in self.portal['portal_controlpanel'].listActions()
        ]
        self.assertIn(
            'imagecropping.settings',
            actions,
            'control panel was not removed'
        )


class TestUninstall(unittest.TestCase):

    layer = IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer is None:
            self.installer = api.portal.get_tool('portal_quickinstaller')
            self.installer.uninstallProducts(
                products=['plone.app.imagecropping'])
        else:
            self.installer = get_installer(self.portal)
            self.installer.uninstall_product('plone.app.imagecropping')

    def test_product_uninstalled(self):
        """Test if plone.app.imagecropping is cleanly uninstalled."""
        if get_installer is None:
            is_installed = self.installer.isProductInstalled(
                'plone.app.imagecropping')
        else:
            is_installed = self.installer.is_product_installed(
                'plone.app.imagecropping')
        self.assertFalse(is_installed)

    def test_browserlayer_removed(self):
        """Test that IPloneAppImagecroppingLayer is removed."""
        from plone.app.imagecropping.interfaces import \
            IPloneAppImagecroppingLayer
        from plone.browserlayer import utils

        self.assertNotIn(
            IPloneAppImagecroppingLayer,
            utils.registered_layers()
        )

    def test_controlpanel_removed(self):
        # controlpanel configlets are not removed but set to invisible
        action = [
            a.getAction(self)
            for a in self.portal['portal_controlpanel'].listActions()
            if a.getAction(self)['id'] == 'imagecropping.settings'
        ]
        self.assertEqual(len(action), 0)
