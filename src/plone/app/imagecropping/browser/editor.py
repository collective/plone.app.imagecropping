# -*- coding: utf-8 -*-
from Acquisition import (
    aq_inner,
)
from zope import component
from zope import interface
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from plone.app.imaging.utils import getAllowedSizes

from plone.app.imagecropping.browser.interfaces import ICroppingEditorView


class CroppingEditor(BrowserView):


    interface.implements(ICroppingEditorView)
    template = ViewPageTemplateFile('editor.pt')

    def scales(self):
        """read interface"""

        context = aq_inner(self.context)
        results = []
        for iface, name in self._fields():
            image_url = "%s/@@images/%s" % (context.absolute_url(),
                                           name)
            item = {'full-image': image_url,
                    'field': name,
                    'title': name,
                    'iface': iface.__identifier__,
                    'scales': self._get_scales(iface, name)}
            results.append(item)
        return results


    def current_image(self):
        """read interface"""
        images = self.scales()
        current_image = images[0]
        current_image['current_scale'] = images[0]['scales'][0]
        current = self.request.form.get('image-select', None)
        if isinstance(current, list):
            current = current[0]
        if current is not None:
            for image in images:
                if current.startswith('%s.%s' %
                                      (image['iface'], image['field'])):
                    current_image = image
                    for scale in image['scales']:
                        if current.endswith(scale['id']):
                            current_image['current_scale'] = scale
        return current_image

    def current_url(self):
        """read interface"""
        context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        return context_state.current_page_url()


    def save(self, x1, y1, x2, y2, scale_name, scale_width, scale_height,
             iface, fieldname):
        """ save a scale
            dummy"""


    def __call__(self):
        form = self.request.form
        if form.get('form.button.Cancel', None) is not None:
            return self.request.response.redirect(
                self.context.absolute_url() + '/view')
        if form.get('form.button.Save', None) is not None:
            all_sizes = getAllowedSizes()
            x1 = int(round(float(self.request.form.get('x1'))))
            y1 = int(round(float(self.request.form.get('y1'))))
            x2 = int(round(float(self.request.form.get('x2'))))
            y2 = int(round(float(self.request.form.get('y2'))))
            scale_name = self.request.form.get('scalename')
            identifier = self.request.form.get('field')
            iface, fieldname = identifier.rsplit('.', 1)
            success = self.save(x1, y1, x2, y2, scale_name,
                                all_sizes[scale_name][0],
                                all_sizes[scale_name][1],
                                iface, fieldname)
            if success:
                # add a success-message here
                pass
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


    def _get_scales(self, iface, name):
        """ get scales for an specific image """
        all_sizes = getAllowedSizes()
        ids = []
        prefix = "%s.%s" % (iface.__identifier__, name)
        current_selected = self.request.get('image-select', '')
        field = self.context.getField(name)
        image_size = field.getSize(self.context)
        for index, size in enumerate(all_sizes):
            min_width, min_height = self._min_size(image_size, all_sizes[size])
            value = '%s-%s' % (prefix, size)
            ids.append({
                'id': size,
                'orig_width': image_size[0],
                'orig_height': image_size[1],
                'ratio_width': all_sizes[size][0],
                'ratio_height': all_sizes[size][1],
                'min_width': min_width,
                'min_height': min_height,
                'max_width': 0,
                'max_height': 0,
                'value': value,
                'selected': value == current_selected and 'selected' or '',
            })
        return ids

    def _fields(self):
        """Returns list of field names."""
        dummy =  [(IATContentType, "image")]
        return dummy
