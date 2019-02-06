# -*- coding: utf-8 -*-
from io import BytesIO
from plone.app.imagecropping.dx import IImageCroppingDX
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imagecropping.storage import Storage
from Products.Five.browser import BrowserView

import PIL.Image


class CroppingView(BrowserView):

    DEFAULT_FORMAT = 'PNG'

    def __call__(self, **kw):
        form = self.request.form
        fieldname = form['fieldname']
        scale_id = form['scale']
        if 'remove' in form:
            storage = Storage(self.context)
            storage.remove(fieldname, scale_id)
            return 'OK'

        box = (
            int(round(float(form['x']))),
            int(round(float(form['y']))),
            int(round(float(form['x']) + float(form['width']))),
            int(round(float(form['y']) + float(form['height']))),
        )
        self._crop(fieldname, scale_id, box)
        return 'OK'

    def _crop(self, fieldname, scale, box):
        """Delegate to store.

        """
        storage = Storage(self.context)
        storage.store(fieldname, scale, box)

        if IImageCroppingDX.providedBy(self.context):
            return
        # AT BBB scaling.
        croputils = IImageCroppingUtils(self.context)
        data = croputils.get_image_data(fieldname)

        original_file = BytesIO(data)
        image = PIL.Image.open(original_file)
        image_format = image.format or self.DEFAULT_FORMAT

        cropped_image = image.crop(box)
        cropped_image_file = BytesIO()
        cropped_image.save(cropped_image_file, image_format, quality=100)
        cropped_image_file.seek(0)

        croputils.save_cropped(fieldname, scale, cropped_image_file)
