from os.path import dirname, join
from plone.app.imagecropping import tests
from plone.app.imagecropping.testing import PLONE_APP_IMAGECROPPING_FUNCTIONAL
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import transaction
import unittest2 as unittest


class TestExample(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        # create test image as testuser
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.portal.invokeFactory('Image', 'testimage',
                                  title=u"I'm a testing Image")
        transaction.commit()

        self.img = self.portal.testimage
        f = file(join(dirname(tests.__file__), 'plone-logo.png'))
        self.img.setImage(f)
        f.close()

        setRoles(self.portal, TEST_USER_ID, ['Authenticated', ])

        # setup testbrowser
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_editorview(self):
        """
        """
        # is there the cropping action tab
        self.browser.open("%s/view" % self.img.absolute_url())
        self.assertTrue("Cropping" in self.browser.contents)

        self.browser.getLink('Cropping').click()
        self.assertTrue(u"Image Cropping Editor" in self.browser.contents)
