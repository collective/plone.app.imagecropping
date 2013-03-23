from Products.CMFPlone.utils import _createObjectByType
from os.path import dirname, join
from plone.app.imagecropping import tests
from plone.app.imagecropping.testing import PLONE_APP_IMAGECROPPING_FUNCTIONAL
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser, installProduct
import transaction
import unittest2 as unittest


class EditorTestCase(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        # setup testbrowser
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def createSingleImageType(self):
        # create test image as testuser
        _createObjectByType('Image', self.portal, 'testimage',
            title=u"I'm a testing Image")
        transaction.commit()

        self.img = self.portal.testimage
        f = file(join(dirname(tests.__file__), 'plone-logo.png'))
        self.img.setImage(f)
        f.close()

    def test_singleimage_editorview(self):
        """ """
        self.createSingleImageType()
        # is there the cropping action tab
        self.browser.open("%s/view" % self.img.absolute_url())
        self.assertTrue("Cropping" in self.browser.contents)

        self.browser.getLink('Cropping').click()
        self.assertTrue(u"Image Cropping Editor" in self.browser.contents)

        # check for non existing image field column
        self.assertFalse(u"Available Image Fields" in self.browser.contents)

        # check for scales column
        self.assertTrue(u"Available Image Scales" in self.browser.contents)

        # check for editor buttons
        self.assertTrue(u"Save" in self.browser.contents)
        self.assertTrue(u"Delete" in self.browser.contents)
        self.assertTrue(u"Cancel" in self.browser.contents)

    def tearDown(self):
        self.portal.manage_delObjects(['testimage', ])
