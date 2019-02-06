# -*- coding: utf-8 -*-
from io import BytesIO
from os.path import dirname
from PIL import Image
from plone.namedfile.file import NamedBlobImage


TEST_IMAGE_FILE = '/'.join([dirname(__file__), u'plone-logo.png'])


def dummy_named_blob_png_image():
    return NamedBlobImage(
        data=open(TEST_IMAGE_FILE, 'rb').read(),
        filename=TEST_IMAGE_FILE
    )


def dummy_named_blob_jpg_image():
    img = Image.open(TEST_IMAGE_FILE)
    out = BytesIO()
    if img.mode in ('RGBA', 'LA'):
        # need to remove the alpha channel for Pillow > 4.1.x
        fill_color = '#FFFFFF'  # your background
        background = Image.new(img.mode[:-1], img.size, fill_color)
        background.paste(img, img.split()[-1])
        img = background
    img.save(out, format='JPEG', quality=75)
    out.seek(0)
    bi = NamedBlobImage(data=out.getvalue())
    out.close()
    return bi
