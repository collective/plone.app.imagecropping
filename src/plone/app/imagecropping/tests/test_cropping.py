import unittest2 as unittest
from os.path import dirname, join
from Products.CMFCore.utils import getToolByName

from plone.app.imagecropping.testing import\
    PLONE_APP_IMAGECROPPING_INTEGRATION
from Products.CMFPlone.utils import _createObjectByType

from plone.app.imagecropping import tests

class TestExample(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        _createObjectByType('Image', self.portal, 'testimage', title="I'm a testing Image")

        self.img = self.portal.testimage
        f = file(join(dirname(tests.__file__), 'plone-logo.png'))
        self.img.setImage(f)
        f.close()




    def test_croppingview(self):
        """
        """

        view = self.img.restrictedTraverse('@@crop-image')
        traverse = self.portal.REQUEST.traverseName

        #check that the image scaled to thumb is not rectangular yet
        self.img.restrictedTraverse('')
        thumb = traverse(self.img, 'image_thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 38))

        #store cropped version for thumb and check if the result is a square now
        view._crop(fieldname='image', scale='thumb', box=(14,14,218,218) )
        thumb = traverse(self.img, 'image_thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 128))
