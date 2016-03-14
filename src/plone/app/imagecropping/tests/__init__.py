# -*- coding: utf-8 -*-
from cStringIO import StringIO
from os.path import dirname
from PIL import Image
from plone.namedfile.file import NamedBlobImage


TEST_IMAGE_FILE = '/'.join([dirname(__file__), u'plone-logo.png'])


def dummy_named_blob_png_image():
    return NamedBlobImage(
        data=open(TEST_IMAGE_FILE, 'r').read(),
        filename=TEST_IMAGE_FILE
    )


def dummy_named_blob_jpg_image():
    img = Image.open(TEST_IMAGE_FILE)
    out = StringIO()
    img.save(out, format='JPEG', quality=75)
    out.seek(0)
    bi = NamedBlobImage(data=out.getvalue())
    out.close()
    return bi
