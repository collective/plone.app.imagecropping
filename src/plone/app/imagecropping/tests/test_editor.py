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

import transaction
import unittest


class EditorTestCase(unittest.TestCase):
    layer = IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]

        # setup testbrowser
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            f"Basic {TEST_USER_NAME:s}:{TEST_USER_PASSWORD:s}",
        )
        self.createSingleImageType()

    def createSingleImageType(self):
        # create test image as testuser
        self.portal.invokeFactory("Image", "testimage", title="I'm a testing Image")
        self.img = self.portal["testimage"]
        self.img.image = dummy_named_blob_png_image()
        self.img.reindexObject()
        transaction.commit()

    def test_editview_crop(self, check_assert=True):
        scale_name = "mini"
        request = self.layer["request"]
        request.form.update(
            {
                "x": 1.0,
                "y": 2.7,
                "width": 9.6,
                "height": 5.7,
                "fieldname": "image",
                "scale": scale_name,
                "form.button.Save": "1",
            }
        )
        cropview = api.content.get_view("crop-image", self.img, request)
        result = cropview()
        self.assertEqual(result, "OK")

        def get_cropped_scale(scales):
            return [s for s in scales if s["id"] == scale_name][0]

        cropedit = api.content.get_view("croppingeditor", self.img, request)
        cropedit()
        cropped_scale = get_cropped_scale(cropedit.scales_info("image"))
        if check_assert:
            self.assertEqual(cropped_scale["is_cropped"], True)

    def test_editview_remove(self, check_assert=True):
        scale_name = "mini"
        request = self.layer["request"]
        request.form.update(
            {
                "remove": 1,
                "fieldname": "image",
                "scale": scale_name,
                "form.button.Save": "1",
            }
        )
        cropview = api.content.get_view("crop-image", self.img, request)
        result = cropview()
        self.assertEqual(result, "OK")

    def test_can_scale(self, check_assert=True):
        scale_name = "teaser"
        request = self.layer["request"]
        request.form.update(
            {
                "x": 1.0,
                "y": 2.7,
                "width": 600,
                "height": 200,
                "fieldname": "image",
                "scale": scale_name,
                "form.button.Save": "1",
            }
        )

        def get_cropped_scale(scales):
            return [s for s in scales if s["id"] == scale_name][0]

        # set teaser target width and height lower than image height (776x232):
        api.portal.set_registry_record(
            "plone.allowed_sizes",
            ["teaser 600:200"],
        )
        cropedit = api.content.get_view("croppingeditor", self.img, request)
        cropedit()
        cropped_scale = get_cropped_scale(cropedit.scales_info("image"))
        if check_assert:
            self.assertTrue(cropped_scale["can_scale"])

        # set teaser target width lower than image width (776x232) and height on max ():
        api.portal.set_registry_record(
            "plone.allowed_sizes",
            ["teaser 600:65536"],
        )
        cropedit = api.content.get_view("croppingeditor", self.img, request)
        cropedit()
        cropped_scale = get_cropped_scale(cropedit.scales_info("image"))
        if check_assert:
            self.assertTrue(cropped_scale["can_scale"])

        # set teaser width higher than image width (776x232):
        api.portal.set_registry_record(
            "plone.allowed_sizes",
            ["teaser 800:200"],
        )
        cropedit = api.content.get_view("croppingeditor", self.img, request)
        cropedit()
        cropped_scale = get_cropped_scale(cropedit.scales_info("image"))
        if check_assert:
            self.assertFalse(cropped_scale["can_scale"])

        # set teaser height higher than image height (776x232):
        api.portal.set_registry_record(
            "plone.allowed_sizes",
            ["teaser 600:400"],
        )
        cropedit = api.content.get_view("croppingeditor", self.img, request)
        cropedit()
        cropped_scale = get_cropped_scale(cropedit.scales_info("image"))
        if check_assert:
            self.assertFalse(cropped_scale["can_scale"])

    def test_events(self):
        sm = getGlobalSiteManager()
        firedEvents = []

        def recordEvent(event):
            firedEvents.append(event.__class__)

        sm.registerHandler(recordEvent, (ICroppingInfoChangedEvent,))
        sm.registerHandler(recordEvent, (ICroppingInfoRemovedEvent,))

        # do some cropping and removing
        self.test_editview_crop(check_assert=False)
        self.assertCountEqual(
            firedEvents,
            [
                CroppingInfoChangedEvent,
            ],
        )

        firedEvents = []
        self.test_editview_remove(check_assert=False)
        self.assertCountEqual(
            firedEvents,
            [
                CroppingInfoRemovedEvent,
            ],
        )

        sm.unregisterHandler(recordEvent, (ICroppingInfoChangedEvent,))
        sm.unregisterHandler(recordEvent, (ICroppingInfoRemovedEvent,))

    def tearDown(self):
        api.content.delete(self.portal.testimage)
