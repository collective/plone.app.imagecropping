# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.imagecropping.testing import PLONE_APP_IMAGECROPPING_INTEGRATION

import unittest


class TestSetup(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'plone.app.imagecropping'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertIn(pid, installed,
                      'package appears not to have been installed')

    def test_css_registered(self):
        cssreg = getattr(self.portal, 'portal_css')
        stylesheets_ids = cssreg.getResourceIds()
        self.assertIn(
            '++resource++plone.app.imagecropping.static/jquery.Jcrop.css',
            stylesheets_ids)
        self.assertIn(
            '++resource++plone.app.imagecropping.static/cropping.css',
            stylesheets_ids)
