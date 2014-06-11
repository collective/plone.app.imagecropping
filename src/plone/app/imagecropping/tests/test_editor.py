# -*- coding: utf-8 -*-
from os.path import dirname
from os.path import join
from plone.app.imagecropping import tests
from plone.app.imagecropping.testing import PLONE_APP_IMAGECROPPING_FUNCTIONAL
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

import transaction
import unittest


class EditorTestCase(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        # setup testbrowser
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {0:s}:{1:s}'.format(TEST_USER_NAME, TEST_USER_PASSWORD)
        )
        self.createSingleImageType()

    def createSingleImageType(self):
        # create test image as testuser
        self.portal.invokeFactory('Image', 'testimage',
                                  title=u'I\'m a testing Image')
        self.img = self.portal['testimage']
        self.img.reindexObject()
        transaction.commit()

        f = file(join(dirname(tests.__file__), 'plone-logo.png'))
        self.img.setImage(f)
        f.close()

    def test_singleimage_editorview(self):
        # is there the cropping action tab
        self.browser.open('{0:s}/view'.format(self.img.absolute_url()))
        self.assertIn('Cropping', self.browser.contents)

        self.browser.getLink('Cropping').click()
        self.assertIn(u'Image Cropping Editor', self.browser.contents)

        # check for non existing image field column
        self.assertNotIn(u'Available Image Fields', self.browser.contents)

        # check for scales column
        self.assertTrue(u'Available Image Scales' in self.browser.contents)

        # check for editor buttons
        self.assertIn(u'Save cropping information', self.browser.contents)
        self.assertIn(u'Remove cropping information', self.browser.contents)

    def test_editview_crop(self):
        request = self.layer['request']
        request.form.update({'x1': 1.0, 'y1': 2.7, 'x2': 10.6, 'y2': 8.4,
                             'scalename': 'mini'})
        cropview = self.img.restrictedTraverse('@@croppingeditor')
        cropview._crop()

    def tearDown(self):
        self.portal.manage_delObjects(['testimage', ])
