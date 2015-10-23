# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from operator import itemgetter
from plone.app.imagecropping import imagecroppingMessageFactory as _
from plone.app.imagecropping.browser.settings import ISettings
from plone.app.imagecropping.events import CroppingInfoChangedEvent
from plone.app.imagecropping.events import CroppingInfoRemovedEvent
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imaging.utils import getAllowedSizes
from plone.registry.interfaces import IRegistry
from zope import component
from zope.component._api import getUtility
from zope.event import notify
from zope.i18n import translate

import json


class CroppingEditor(BrowserView):
    """ Cropping Editor View """

    template = ViewPageTemplateFile('editor.pt')

    default_cropping_max_size = (0, 0)

    @property
    def croputils(self):
        return IImageCroppingUtils(self.context)

    @property
    def default_editor_size(self):
        return self._editor_settings.large_size.split(':')

    @property
    def showCropping(self):
        """returns True if there are any croppable scales on any of the fields
        """
        for field in self.image_field_names():
            if len(self.scales(field)) > 0:
                return True
        return False

    @property
    def fieldname(self):
        if 'fieldname' in self.request.form.keys():
            # TODO: check if requested fieldname is available
            # in self.image_fields
            return self.request.form.get('fieldname')

        img_field_names = self.image_field_names()
        return len(img_field_names) > 0 and img_field_names[0]

    def scales(self, fieldname=None):
        """Returns information to initialize JCrop for all available scales
           on the current content with the given fieldname and interface."""

        scales = []
        cropview = self.context.restrictedTraverse('@@crop-image')
        if fieldname is None:
            fieldname = self.fieldname
        image_size = self.croputils.get_image_size(fieldname)
        all_sizes = getAllowedSizes()
        current_selected = self.request.get('scalename', None)
        large_image_url = self.image_url(fieldname)
        constrain_cropping = self._editor_settings.constrain_cropping
        cropping_for = self._editor_settings.cropping_for
        for size, dim in sorted(all_sizes.iteritems(), key=itemgetter(1)):
            if constrain_cropping and size not in cropping_for:
                continue
            scale = dict()
            # scale jcrop config
            min_width, min_height = self._min_size(image_size, dim)
            max_width, max_height = self.default_cropping_max_size[0], \
                self.default_cropping_max_size[1]
            ratio_width, ratio_height = dim[0], dim[1]

            # lookup saved crop info
            select_box = cropview._read(fieldname, size)
            is_cropped = True

            if select_box is None:
                select_box = self._initial_size(image_size, dim)
                is_cropped = False

            config = dict([
                ('allowResize', True),
                ('allowMove', True),
                ('trueSize', [image_size[0], image_size[1]]),
                ('boxWidth', self.default_editor_size[0]),
                ('boxHeight', self.default_editor_size[1]),
                ('setSelect', select_box),
                ('aspectRatio', '%.2f' % (
                    float(ratio_width) / float(ratio_height))),
                ('minSize', [min_width, min_height]),
                ('maxSize', [max_width, max_height]),
                ('imageURL', large_image_url),
            ])
            scale['config'] = json.dumps(config)
            # scale value/id
            scale['id'] = size
            scale['title'] = '{0:s} {1:s}'.format(size, dim)
            scale['selected'] = size == current_selected and 'selected' or ''
            # flag if saved cropped scale was found
            # this helps to prevent generating unused
            # default scales in preview column
            scale['is_cropped'] = is_cropped
            # TODO: this is for thumbnail live-preview
            scale['thumb_width'] = ratio_width
            scale['thumb_height'] = ratio_height
            # safe original image url
            scale['image_url'] = large_image_url

            scales.append(scale)
        return scales

    def image_field_names(self):
        return self.croputils.image_field_names()

    def current_scale(self):
        """Returns information of the current selected scale"""
        images = self.scales()
        current_image = images[0]
        current = self.request.form.get('scalename', None)
        if isinstance(current, list):
            current = current[0]
        if current is not None:
            for image in images:
                if image['id'] == current:
                    current_image = image
        return current_image

    def current_url(self):
        """Returns the current page url"""
        context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        return context_state.current_page_url()

    def image_url(self, fieldname):
        """Returns the url to the unscaled image"""
        scales = self.context.restrictedTraverse('@@images')
        scaled_img = scales.scale(
            fieldname,
            width=int(self.default_editor_size[0]),
            height=int(self.default_editor_size[1]),
            direction='keep',
        )
        return scaled_img and scaled_img.url or ''

    def field_label(self, fieldname):
        return self.croputils.get_image_label(fieldname)

    def _crop(self):
        coordinate = lambda x: int(round(float(self.request.form.get(x))))
        x1 = coordinate('x1')
        y1 = coordinate('y1')
        x2 = coordinate('x2')
        y2 = coordinate('y2')
        scale_name = self.request.form.get('scalename')
        cropping_util = self.context.restrictedTraverse('@@crop-image')
        cropping_util._crop(fieldname=self.fieldname,
                            scale=scale_name,
                            box=(x1, y1, x2, y2))

    def __call__(self):
        form = self.request.form
        if form.get('form.button.Delete', None) is not None:
            cropping_util = self.context.restrictedTraverse('@@crop-image')
            cropping_util._remove(self.fieldname, form.get('scalename'))
            nofity(CroppingInfoRemovedEvent(self.context))
            IStatusMessage(self.request).add(_(u'Cropping area deleted'))
        if form.get('form.button.Save', None) is not None:
            self._crop()
            notify(CroppingInfoChangedEvent(self.context))
            IStatusMessage(self.request).add(
                _(u'Successfully saved cropped area'))

        # disable columns
        self.request.set('disable_plone.leftcolumn', 1)
        self.request.set('disable_plone.rightcolumn', 1)

        return self.template()

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
        """we need a best fit centered preselection to make editots life
        better.
        """
        ix, iy = map(float, image_size)

        # aspect ratio of original
        if iy > 0:
            ir = ix / iy
        else:
            ir = 1

        sx, sy = map(float, scale_size)

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

    @property
    def _editor_settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        return settings

    @property
    def translated_confirm_discard_changes(self):
        # Escape for javascript
        return translate(
            _(u'Your changes will be lost. Continue?'),
            target_language=self.request.get('LANGUAGE', 'en'),
        ).replace('\'', '\\\'')
