# -*- coding: utf-8 -*-
from cStringIO import StringIO
from logging import exception
from logging import getLogger

from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imaging.interfaces import IImagingSchema
from zope.component.hooks import getSite
from zope.annotation.interfaces import IAnnotations
from ZODB.POSException import ConflictError

try:
    import PIL.Image
    from plone.scale.scale import scaleImage
except ImportError:
    logger = getLogger('plone.app.imaging')
    logger.warn("Warning: no Python Imaging Libraries (PIL) found. "
                "Can't scale images.")


class ScalingOverrides(object):

    _allow_rescale = True
    DEFAULT_FORMAT = 'PNG'
    _scale_name = None

    def _need_rescale(self, fieldname, scale):
        """If we've got a cropping annotation for the given fieldname
           and scale, set self._allow_rescale to False, to prevent
           plone.app.imaging traverser to overwrite our cropped scale

           since the self.modified() method does not know about the
           currently requested scale name, we need to use the _allow_rescale
           property
        """
        if self._get_crop_box(fieldname, scale):
            self._allow_rescale = False
        else:
            self._allow_rescale = True

    def _get_crop_box(self, fieldname, scale):
        cropped = IAnnotations(self.context).get(PAI_STORAGE_KEY)
        if cropped:
            return cropped.get('{0:s}_{1:s}'.format(fieldname, scale))

    def _wrap_image(self, data, fmt='PNG', fieldname=None):
        return data

    def _cropped_image(self, fieldname, box, direction='keep', **parameters):
        croputils = IImageCroppingUtils(self.context)
        data = croputils.get_image_data(fieldname)

        original_file = StringIO(data)
        image = PIL.Image.open(original_file)
        image_format = image.format or self.DEFAULT_FORMAT

        cropped_image = image.crop(box)
        cropped_image_file = StringIO()
        cropped_image.save(cropped_image_file, image_format, quality=100)
        cropped_image_file.seek(0)

        if 'quality' not in parameters:
            imaging_schema = IImagingSchema(getSite())
            parameters['quality'] = getattr(imaging_schema, 'quality', None)

        data, fmt, size = scaleImage(cropped_image_file, direction=direction,
                                     **parameters)

        return self._wrap_image(data, fmt, fieldname), fmt, size

    def create(self, fieldname, direction='keep', **parameters):
        """ override factory for image scale creation to perform cropping,
            when a crop is set """
        if self._scale_name:
            scale = self._scale_name
            box = self._get_crop_box(fieldname, scale)
            if box is not None:
                try:
                    return self._cropped_image(fieldname, box, direction,
                                               **parameters)
                except (ConflictError, KeyboardInterrupt):
                    raise
                except Exception:
                    exception('could not scale "%r" of %r',
                              fieldname, self.context.absolute_url())
        return super(ScalingOverrides, self).create(fieldname, direction,
                                                    **parameters)
