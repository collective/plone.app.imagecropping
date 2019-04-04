# -*- coding: utf-8 -*-
from plone import api
from plone.app.imagecropping.events import CroppingInfoChangedEvent
from plone.app.imagecropping.events import CroppingInfoRemovedEvent
from plone.app.imagecropping.interfaces import ICroppingInfoChangedEvent
from plone.app.imagecropping.interfaces import ICroppingInfoRemovedEvent
from plone.app.imagecropping.testing import IMAGECROPPING_FUNCTIONAL
from plone.app.imagecropping.tests import dummy_named_blob_png_image
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from zope.component import getGlobalSiteManager

import six
import transaction
import unittest


class EditorTestCase(unittest.TestCase):

    layer = IMAGECROPPING_FUNCTIONAL

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
        self.portal.invokeFactory(
            'Image',
            'testimage',
            title=u'I\'m a testing Image'
        )
        self.img = self.portal['testimage']
        self.img.image = dummy_named_blob_png_image()
        self.img.reindexObject()
        transaction.commit()

    def test_editview_crop(self, check_assert=True):
        scale_name = 'mini'
        request = self.layer['request']
        request.form.update({
            'x': 1.0, 'y': 2.7, 'width': 9.6, 'height': 5.7,
            'fieldname': 'image',
            'scale': scale_name, 'form.button.Save': '1'})
        cropview = api.content.get_view('crop-image', self.img, request)
        result = cropview()
        self.assertEqual(result, 'OK')

        def get_cropped_scale(scales):
            return [s for s in scales if s['id'] == scale_name][0]

        cropedit = api.content.get_view('croppingeditor', self.img, request)
        cropedit()
        cropped_scale = get_cropped_scale(cropedit.scales_info('image'))
        if check_assert:
            self.assertEqual(cropped_scale['is_cropped'], True)

    def test_editview_remove(self, check_assert=True):
        scale_name = 'mini'
        request = self.layer['request']
        request.form.update({
            'remove': 1,
            'fieldname': 'image',
            'scale': scale_name, 'form.button.Save': '1'})
        cropview = api.content.get_view('crop-image', self.img, request)
        result = cropview()
        self.assertEqual(result, 'OK')

    def test_events(self):
        sm = getGlobalSiteManager()
        firedEvents = []

        def recordEvent(event):
            firedEvents.append(event.__class__)

        sm.registerHandler(recordEvent, (ICroppingInfoChangedEvent,))
        sm.registerHandler(recordEvent, (ICroppingInfoRemovedEvent,))

        # do some cropping and removing
        self.test_editview_crop(check_assert=False)
        self.test_editview_remove(check_assert=False)

        six.assertCountEqual(self, firedEvents, [
            CroppingInfoChangedEvent,
            CroppingInfoRemovedEvent,
        ])
        sm.unregisterHandler(recordEvent, (ICroppingInfoChangedEvent,))
        sm.unregisterHandler(recordEvent, (ICroppingInfoRemovedEvent,))

    def tearDown(self):
        api.content.delete(self.portal.testimage)
