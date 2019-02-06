# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.testing import IMAGECROPPING_FUNCTIONAL
from plone.app.imagecropping.tests import dummy_named_blob_jpg_image
from plone.app.imagecropping.tests import dummy_named_blob_png_image
from Products.CMFPlone.utils import _createObjectByType
from unittest.case import skip
from zope import event
from zope.annotation.interfaces import IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestCroppingDX(unittest.TestCase):

    layer = IMAGECROPPING_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        _createObjectByType(
            'Image',
            self.portal,
            'testimage',
            title='I\'m a testing Image'
        )

        self.img = self.portal.testimage
        self.img.image = dummy_named_blob_png_image()

    def test_image_and_annotation(self):
        """Check that our cropping view is able to store a cropped image
           and also saves the crop-box info in an annotation
        """

        view = self.img.restrictedTraverse('@@crop-image')
        traverse = self.portal.REQUEST.traverseName

        # check that the image scaled to thumb is not rectangular yet
        self.img.restrictedTraverse('')
        scales = traverse(self.img, '@@images')
        thumb = scales.scale('image', 'thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 38))

        # there is also no annotations yet for cropped sizes on this image
        self.assertEqual(
            IAnnotations(self.img).get(PAI_STORAGE_KEY),
            {},
            'fresh image should not have any annotations'
        )

        # store cropped version for thumb and check if the result
        # is a square now
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        thumb = scales.scale('image', 'thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 128))

        # when storing a new crop-scale the crop-box information is
        # stored as an annotation.
        # this allows us to fire up the editor with the correct box when
        # editing the scale and it also allows us to identify if a scale
        # is cropped or simply resized
        self.assertEqual(
            list(IAnnotations(self.img).get(PAI_STORAGE_KEY).keys()),
            ['image_thumb'],
            'there\'s only one scale that is cropped'
        )
        self.assertEqual(
            IAnnotations(self.img).get(PAI_STORAGE_KEY)['image_thumb'],
            (14, 14, 218, 218),
            'wrong box information has been stored'
        )

    def test_accessing_images(self):
        """Test if accessing the images works for our users
        """

        view = self.img.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))

        # another use-case: call plone.app.imaging's ImageScaling view
        scales = self.img.restrictedTraverse('@@images')
        thumb2 = scales.scale('image', 'thumb')
        self.assertEqual(
            (thumb2.width, thumb2.height),
            (128, 128),
            'imagescaling does not return cropped image'
        )

    def test_image_formats(self):
        """make sure the scales have the same format as the original image
        """

        from io import BytesIO
        from PIL.Image import open
        org_data = BytesIO(self.img.image.data)
        self.assertEqual(open(org_data).format, 'PNG')

        view = self.img.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        traverse = self.portal.REQUEST.traverseName

        scales = traverse(self.img, '@@images')
        cropped = scales.scale('image', 'thumb')
        croppedData = BytesIO(cropped.data._data)
        self.assertEqual(
            open(croppedData).format,
            'PNG',
            'cropped scale does not have same format as the original'
        )

        # create a jpeg image out of the png file
        # and test if created scale is jpeg too
        _createObjectByType('Image', self.portal, 'testjpeg')
        jpg = self.portal.testjpeg
        jpg.image = dummy_named_blob_jpg_image()

        org_data = BytesIO(jpg.image.data)
        self.assertEqual(open(org_data).format, 'JPEG')

        view = jpg.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        cropped = scales.scale('image', 'thumb')
        croppedData = BytesIO(cropped.data._data)

        # XXX: fixme
        # self.assertEqual(open(croppedData).format, 'JPEG',
        #    "cropped scale does not have same format as the original")

    def test_modify_context(self):
        """ See https://github.com/collective/plone.app.imagecropping/issues/21
        """

        view = self.img.restrictedTraverse('@@crop-image')
        traverse = self.portal.REQUEST.traverseName
        scales = traverse(self.img, '@@images')
        unscaled_thumb = scales.scale('image', 'thumb')

        # store cropped version for thumb and check if the result
        # is a square now
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))

        # images accessed via context/@@images/image/thumb
        # stored in plone.scale annotation
        # see https://github.com/plone/plone.scale/pull/3#issuecomment-28597087
        thumb = scales.scale('image', 'thumb')
        self.assertNotEqual(thumb.data._data, unscaled_thumb.data._data)

        # XXX: traversal does not seem to work in the DX test fixture
        # # images accessed via context/image_thumb
        # # stored in attribute_storage
        # thumb_attr = traverse(self.img, 'image_thumb')
        # self.assertNotEqual(thumb_attr.data, unscaled_thumb.data)
        # self.assertEqual(
        #     (thumb.width, thumb.height),
        #     (thumb_attr.width, thumb_attr.height)
        # )

        self.img.setTitle('A new title')
        self.img.reindexObject()

        thumb2 = scales.scale('image', 'thumb')
        self.assertEqual(
            thumb.data._data,
            thumb2.data._data,
            'context/@@images/image/thumb accessor lost cropped scale'
        )

        # XXX: traversal does not seem to work in the DX test fixture
        # thumb2_attr = traverse(self.img, 'image_thumb')
        # self.assertEqual(
        #     (thumb.width, thumb.height),
        #     (thumb2_attr.width, thumb2_attr.height),
        #     'context/image_thumb accessor lost cropped scale'
        # )

    @skip('currently fails - see #54')
    def test_modify_image(self):
        """set a different image, this should invalidate scales

        see and https://github.com/collective/plone.app.imagecropping/issues/54
        """

        view = self.img.restrictedTraverse('@@crop-image')
        traverse = self.portal.REQUEST.traverseName
        scales = traverse(self.img, '@@images')

        # store cropped version for thumb and check if the result
        # is a square now
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        cropped = scales.scale('image', 'thumb')
        self.assertEqual((cropped.width, cropped.height), (128, 128))

        # upload another image file
        self.img.image = dummy_named_blob_jpg_image()
        event.notify(ObjectModifiedEvent(self.img))

        # XXX: traversal does not seem to work in the DX test fixture
        # jpeg_thumb_attr = traverse(self.img, 'image_thumb')
        # self.assertNotEqual(
        #     (jpeg_thumb_attr.width, jpeg_thumb_attr.height),
        #     (128, 128),
        #     'context/image_thumb returns old cropped scale after '
        #     'setting a new image'
        # )

        jpeg_thumb = scales.scale('image', 'thumb')
        self.assertNotEqual(
            (jpeg_thumb.width, jpeg_thumb.height),
            (128, 128),
            'context/@@images/image/thumb returns old cropped scale after '
            'setting a new image'
        )

    def test_copy_context(self):
        """ See https://github.com/collective/plone.app.imagecropping/issues/21
        """

        org_view = self.img.restrictedTraverse('@@crop-image')
        traverse = self.portal.REQUEST.traverseName
        org_scales = traverse(self.img, '@@images')
        org_unscaled_thumb = org_scales.scale('image', 'thumb')

        # store cropped version for thumb and check if the result
        # is a square now
        org_view._crop(
            fieldname='image',
            scale='thumb',
            box=(14, 14, 218, 218)
        )

        org_thumb = org_scales.scale('image', 'thumb')
        self.assertNotEqual(org_thumb.data, org_unscaled_thumb.data)

        # XXX: traversal does not seem to work in the DX test fixture
        # # images accessed via context/image_thumb
        # # stored in attribute_storage
        # org_thumb_attr = traverse(self.img, 'image_thumb')
        # self.assertNotEqual(org_thumb_attr.data, org_unscaled_thumb.data)
        # self.assertEqual(
        #     (org_thumb.width, org_thumb.height),
        #     (org_thumb_attr.width, org_thumb_attr.height)
        # )

        # Copy image
        container = aq_parent(self.img)
        container.manage_pasteObjects(
            container.manage_copyObjects(ids=[self.img.id, ]))

        # Be sure copied image is there
        self.assertIn('copy_of_testimage', container.objectIds())

        copy_img = container['copy_of_testimage']
        copy_scales = traverse(copy_img, '@@images')
        copy_thumb = copy_scales.scale('image', 'thumb')
        self.assertEqual(
            org_thumb.data._data,
            copy_thumb.data._data,
            'new thumb is different from old thumb scale after '
            'copying image (@@images access)'
        )

        # XXX: traversal does not seem to work in the DX test fixture
        # copy_thumb_attr = traverse(copy_img, 'image_thumb')
        # self.assertEqual(
        #     org_thumb_attr.data,
        #     copy_thumb_attr.data,
        #     'new thumb is different from old thumb scale after '
        #     'copying image (attribute access)'
        # )

    def test_autocrop(self):
        """ check direction='down' for cropped and un-cropped image scales
        """
        traverse = self.portal.REQUEST.traverseName

        # auto-cropped scale
        img_scales = traverse(self.img, '@@images')
        auto_crop = img_scales.scale('image', 'thumb', direction='down')

        # cropped scale
        view = self.img.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(0, 0, 200, 200))
        manual_crop = img_scales.scale('image', 'thumb', direction='down')
        self.assertEqual(
            (auto_crop.width, auto_crop.height),
            (manual_crop.width, manual_crop.height))
        self.assertNotEqual(auto_crop.data, manual_crop.data)
