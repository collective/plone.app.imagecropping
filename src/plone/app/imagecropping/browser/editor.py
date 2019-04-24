# -*- coding: utf-8 -*-
from operator import itemgetter
from plone import api
from plone.app.imagecropping.browser.settings import ISettings
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imagecropping.storage import Storage
from plone.namedfile.interfaces import IAvailableSizes
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component._api import getUtility
import six
from six.moves import map


class CroppingEditor(BrowserView):
    """ Cropping Editor View """

    def __init__(self, context, request):
        super(CroppingEditor, self).__init__(context, request)
        request.set('disable_plone.leftcolumn', 1)
        request.set('disable_plone.rightcolumn', 1)

    @property
    def _croputils(self):
        return IImageCroppingUtils(self.context)

    @property
    def _editor_settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        return settings

    @property
    def show_cropping(self):
        """returns True if there are any croppable scales on any of the fields
        """
        for fieldname in self.image_field_names:
            for value in self._scales(fieldname):
                return True
        return False

    def _min_size(self, image_size, scale_size):
        """ we need lower min-sizes if the image is smaller than the scale """
        width = scale_size[0]
        height = scale_size[1]
        if width > image_size[0]:
            ratio = float(image_size[0]) / float(width)
            width = image_size[0]
            height = float(height) * ratio
        if height > image_size[1]:
            ratio = float(image_size[1]) / float(height)
            height = image_size[1]
            width = float(width) * ratio
        return (int(round(width)), int(round(height)))

    def _initial_size(self, image_size, scale_size):
        """we need a best fit centered preselection to make editors life
        better.
        """
        ix, iy = list(map(float, image_size))

        # aspect ratio of original
        if iy > 0:
            ir = ix / iy
        else:
            ir = 1

        sx, sy = list(map(float, scale_size))

        # aspect ratio of scale
        if sy > 0:
            sr = sx / sy
        else:
            sr = 1

        # scale up to bounds
        if ir > sr:
            rx1, ry1 = ix * sr / ir, iy
        else:
            rx1, ry1 = ix, iy * ir / sr

        rx0, ry0 = 0, 0

        # center box
        if rx1 < ix:
            deltax = ix - rx1
            rx0 = deltax / 2
            rx1 = rx1 + deltax / 2
        if ry1 < iy:
            deltay = iy - ry1
            ry0 = deltay / 2
            ry1 = ry1 + deltay / 2

        # round to int
        rx0, ry0 = int(round(rx0)), int(round(ry0))
        rx1, ry1 = int(round(rx1)), int(round(ry1))
        return rx0, ry0, rx1, ry1

    def _scale_info(self, fieldname, scale_id, target_size, true_size):
        scale = dict()
        scale['id'] = scale_id
        scale['title'] = scale_id

        # scale config
        min_width, min_height = self._min_size(true_size, target_size)

        # lookup saved crop info
        storage = Storage(self.context)
        current_box = storage.read(fieldname, scale_id)

        if current_box is None:
            current_box = self._initial_size(true_size, target_size)
            scale['is_cropped'] = False
        else:
            scale['is_cropped'] = True

        # images original dimensions
        scale['true_width'] = true_size[0]
        scale['true_height'] = true_size[1]

        # images target dimensions
        scale['target_width'] = target_size[0]
        scale['target_height'] = target_size[1]

        # current selected crop
        scale['current'] = {
            'x': current_box[0],
            'y': current_box[1],
            'w': current_box[2] - current_box[0],
            'h': current_box[3] - current_box[1],
        }
        scale['aspect_ratio'] = '1.777778'  # 16:9
        if target_size[0] > 0 and target_size[1] > 0:
            scale['aspect_ratio'] = '{0:.2f}'.format(
                float(target_size[0]) / float(target_size[1])
            )
        scale['can_scale'] = (
            target_size[0] <= true_size[0] and
            target_size[1] <= true_size[1]
        )
        return scale

    def _scales(self, fieldname):
        constrain_cropping = self._editor_settings.constrain_cropping
        cropping_for = self._editor_settings.cropping_for
        allowed_sizes = getUtility(IAvailableSizes)() or []
        sizes_iterator = sorted(
            six.iteritems(allowed_sizes),
            key=itemgetter(1)
        )
        for scale_id, target_size in sizes_iterator:
            if constrain_cropping and scale_id not in cropping_for:
                continue
            yield scale_id, target_size

    def scales_info(self, fieldname):
        """Returns information to initialize pattern for all available scales
           on the current content with the given fieldname and interface."""
        true_size = self._croputils.get_image_size(fieldname)
        for scale_id, target_size in self._scales(fieldname):
            yield self._scale_info(
                fieldname,
                scale_id,
                target_size,
                true_size
            )

    @property
    def image_field_names(self):
        return self._croputils.image_field_names()

    def icon_url(self, fieldname):
        scales = api.content.get_view('images', self.context, self.request)
        scaled_img = scales.scale(
            fieldname,
            scale='icon',
            direction='keep',
        )
        return scaled_img and scaled_img.url or ''

    def original_url(self, fieldname):
        """Returns the url to the unscaled image"""
        url = self.context.absolute_url()
        return '{0}/@@images/{1}'.format(url, fieldname)

    def field_label(self, fieldname):
        return self._croputils.get_image_label(fieldname)
