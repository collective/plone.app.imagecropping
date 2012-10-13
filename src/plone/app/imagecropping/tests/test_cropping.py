import unittest2 as unittest
import os
from Products.CMFCore.utils import getToolByName

from plone.app.imagecropping.testing import\
    PLONE_APP_IMAGECROPPING_INTEGRATION
from Products.CMFPlone.utils import _createObjectByType


class TestExample(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        _createObjectByType('Image', self.portal, 'testimage', title="I'm a testing Image")


        #there might be a more elegant way to do that
        self.img = self.portal.testimage
        import plone.app.imagecropping.tests as testmodule
        modpath = os.path.dirname(testmodule.__file__)
        filepath = os.path.join(modpath, 'plone-logo.png')
        f = file(filepath)
        self.img.setImage(f)
        f.close()




    def test_croppingview(self):
        """
        """

        view = self.img.restrictedTraverse('@@crop-image')
        import pdb;pdb.set_trace()

