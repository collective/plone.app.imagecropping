# -*- coding: utf-8 -*-
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.imagecropping import imagecroppingMessageFactory as _
from plone.app.imagecropping.browser.settings import ISettings
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.app.imaging.utils import getAllowedSizes
from plone.registry.interfaces import IRegistry
from zope import component
from plone.app.uuid.utils import uuidToObject
from zope.component._api import getUtility
import json


class CroppingEditor(BrowserView):
    """ Cropping Editor View """

    template = ViewPageTemplateFile('editor.pt')

    interface = IATContentType
    default_cropping_max_size = (0, 0)

    @property
    def default_editor_size(self):
        return self._editor_settings.large_size.split(":")

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
        croputils = IImageCroppingUtils(self.context)
        cropview = self.context.restrictedTraverse('@@crop-image')
        if fieldname is None:
            fieldname = self.fieldname
        image_size = croputils.get_image_size(fieldname, self.interface)
        all_sizes = getAllowedSizes()
        current_selected = self.request.get('scalename', all_sizes.keys()[0])
        large_image_url = self.image_url(fieldname)
        constrain_cropping = self._editor_settings.constrain_cropping
        cropping_for = self._editor_settings.cropping_for

        for size in all_sizes:
            if constrain_cropping and size not in cropping_for:
                continue
            scale = dict()
            # scale jcrop config
            min_width, min_height = self._min_size(image_size, all_sizes[size])
            max_width, max_height = self.default_cropping_max_size[0], \
                self.default_cropping_max_size[1]
            ratio_width, ratio_height = all_sizes[size][0], all_sizes[size][1]

            # lookup saved crop info
            select_box = cropview._read(fieldname, size)
            is_cropped = True

            if select_box is None:
                select_box = (0, 0, min_width, min_height)
                is_cropped = False

            config = dict([
                ("allowResize", True),
                ("allowMove", True),
                ("trueSize", [image_size[0], image_size[1]]),
                ("boxWidth", self.default_editor_size[0]),
                ("boxHeight", self.default_editor_size[1]),
                ("setSelect", select_box),
                ("aspectRatio", "%.2f" % (
                    float(ratio_width) / float(ratio_height))),
                ("minSize", [min_width, min_height]),
                ("maxSize", [max_width, max_height]),
                ("imageURL", large_image_url),
            ])
            scale["config"] = json.dumps(config)
            # scale value/id
            scale["id"] = size
            scale["title"] = "%s %s" % (size, all_sizes[size])
            scale["selected"] = size == current_selected and 'selected' or ''
            # flag if saved cropped scale was found
            # this helps to prevent generating unused
            # default scales in preview column
            scale["is_cropped"] = is_cropped
            # TODO: this is for thumbnail live-preview
            scale["thumb_width"] = ratio_width
            scale["thumb_height"] = ratio_height
            # safe original image url
            scale["image_url"] = large_image_url

            scales.append(scale)
        return scales

    def image_fields(self):
        return IImageCroppingUtils(self.context).image_fields()

    def image_field_names(self):
        return IImageCroppingUtils(self.context).image_field_names()

    def current_scale(self):
        """Returns information of the current selected scale"""
        images = self.scales()
        current_image = images[0]
        current = self.request.form.get('scalename', None)
        if isinstance(current, list):
            current = current[0]
        if current is not None:
            for image in images:
                if image["id"] == current:
                    current_image = image
        return current_image

    def current_url(self):
        """Returns the current page url"""
        context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        return context_state.current_page_url()

    def image_url(self, fieldname="image"):
        """Returns the url to the unscaled image"""
        scales = self.context.restrictedTraverse('@@images')
        scaled_img = scales.scale(fieldname,
            width=int(self.default_editor_size[0]),
            height=int(self.default_editor_size[1]))
        return scaled_img and scaled_img.url or ''

    def __call__(self):
        form = self.request.form
        cropping_util = self.context.restrictedTraverse('@@crop-image')

        if form.get('form.button.Cancel', None) is not None:
            if self.request.form.get("came_from", None):
                came_from = self.request.form.get("came_from")
                return self.request.response.redirect(
                    uuidToObject(came_from).absolute_url())
            return self.request.response.redirect(
                self.context.absolute_url() + '/view')
        if form.get('form.button.Delete', None) is not None:
            cropping_util._remove(self.fieldname,
                self.request.form.get('scalename'))
            IStatusMessage(self.request).add(_(u"Cropping area deleted"))
        if form.get('form.button.Save', None) is not None:
            x1 = int(round(float(self.request.form.get('x1'))))
            y1 = int(round(float(self.request.form.get('y1'))))
            x2 = int(round(float(self.request.form.get('x2'))))
            y2 = int(round(float(self.request.form.get('y2'))))
            scale_name = self.request.form.get('scalename')
            cropping_util._crop(fieldname=self.fieldname,
                                scale=scale_name,
                                box=(x1, y1, x2, y2),
                                interface=self.interface)
            IStatusMessage(self.request).add(
                _(u"Successfully saved cropped area"))

        # disable columns
        self.request.set('disable_plone.leftcolumn', 1)
        self.request.set('disable_plone.rightcolumn', 1)

        return self.template()

    def go_back_url(self):
        if self.request.form.get('form.button.Save', None) is not None \
                or self.request.form.get('form.button.Delete', None) \
                is not None:
            if self.request.form.get("came_from", None):
                came_from = self.request.form.get("came_from")
                if uuidToObject(came_from):
                    return uuidToObject(came_from).absolute_url()

    def go_back_title(self):
        if self.request.form.get('form.button.Save', None) is not None \
                or self.request.form.get('form.button.Delete', None) is \
                not None:
            if self.request.form.get("came_from", None):
                came_from = self.request.form.get("came_from")
                if uuidToObject(came_from):
                    return _(u"Go back to ") + uuidToObject(came_from).title

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

    @property
    def _editor_settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        return settings
