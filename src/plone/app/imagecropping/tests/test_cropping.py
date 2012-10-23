from Products.CMFPlone.utils import _createObjectByType
from os.path import dirname, join
from plone.app.imagecropping import tests, PAI_STORAGE_KEY
from plone.app.imagecropping.testing import PLONE_APP_IMAGECROPPING_INTEGRATION
import unittest2 as unittest
from zope.annotation.interfaces import IAnnotations


class TestExample(unittest.TestCase):

    layer = PLONE_APP_IMAGECROPPING_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        _createObjectByType('Image', self.portal, 'testimage',
                            title="I'm a testing Image")

        self.img = self.portal.testimage
        f = file(join(dirname(tests.__file__), 'plone-logo.png'))
        self.img.setImage(f)
        f.close()

    def test_image_and_annotation(self):
        """check that our cropping view is able to store a cropped image
        and also saves the crop-box info in an annotation
        """

        view = self.img.restrictedTraverse('@@crop-image')
        traverse = self.portal.REQUEST.traverseName

        # check that the image scaled to thumb is not rectangular yet
        self.img.restrictedTraverse('')
        thumb = traverse(self.img, 'image_thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 38))

        #there is also no annotations yet for cropped sizes on this image
        self.assertIsNone(IAnnotations(self.img).get(PAI_STORAGE_KEY),
                         "fresh image should not have any annotations")

        # store cropped version for thumb and check if the result
        # is a square now
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        thumb = traverse(self.img, 'image_thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 128))

        # when storing a new crop-scale the crop-box information is stored
        # as an annotation.
        # this allows us to fire up the editor with the correct box when
        # editing the scale and it also allows us to identify if a scale is
        # cropped or simply resized
        self.assertEqual(IAnnotations(self.img).get(PAI_STORAGE_KEY).keys(),
                         ['image_thumb'],
                         "there's only one scale that is cropped")
        self.assertEqual(
            IAnnotations(self.img).get(PAI_STORAGE_KEY)['image_thumb'],
            (14, 14, 218, 218), "wrong box information has been stored")

    def test_accessing_images(self):
        """test if accessing the images works for our users
        """

        view = self.img.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        traverse = self.portal.REQUEST.traverseName

        # one way to access the cropped image is via the traverser
        # <fieldname>_<scalename>
        thumb = traverse(self.img, 'image_thumb')
        self.assertEqual((thumb.width, thumb.height), (128, 128))

        # another is to use plone.app.imaging's ImageScaling view
        scales = traverse(self.img, '@@images')
        thumb2 = scales.scale('image', 'thumb')
        self.assertEqual((thumb2.width, thumb2.height), (128, 128),
            "imagescaling does not return cropped image")

    def test_image_formats(self):
        """make sure the scales have the same format as the original image
        """

        from cStringIO import StringIO
        from PIL.Image import open
        org_data = StringIO(self.img.getImage().data)
        self.assertEqual(open(org_data).format, 'PNG')

        view = self.img.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        traverse = self.portal.REQUEST.traverseName
        cropped = traverse(self.img, 'image_thumb')
        croppedData = StringIO(cropped.data)
        self.assertEqual(open(croppedData).format, 'PNG',
            "cropped scale does not have same format as the original")

        #create a jpeg image out of the png file:
        img = open(file(join(dirname(tests.__file__), 'plone-logo.png')))
        out = StringIO()
        img.save(out, format='JPEG', quality=75)
        out.seek(0)

        #and test if created scale is jpeg too
        _createObjectByType('Image', self.portal, 'testjpeg')
        jpg = self.portal.testjpeg
        jpg.setImage(out.getvalue())

        org_data = StringIO(jpg.getImage().data)
        self.assertEqual(open(org_data).format, 'JPEG')

        view = jpg.restrictedTraverse('@@crop-image')
        view._crop(fieldname='image', scale='thumb', box=(14, 14, 218, 218))
        cropped = traverse(self.img, 'image_thumb')
        croppedData = StringIO(cropped.data)
        self.assertEqual(open(croppedData).format, 'JPEG',
            "cropped scale does not have same format as the original")
