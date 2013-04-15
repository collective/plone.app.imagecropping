'''
Created on 15.04.2013

@author: peterm
'''
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import _checkPermission
from plone.app.uuid.utils import uuidToObject
from plone.outputfilters.interfaces import IFilter
from zope.component import adapter
from zope.interface import Interface, implementer
from zope.publisher.interfaces import IRequest
import re


img_tag = re.compile(r"<img[^>]*>")
src_attr = re.compile(r'src="([^"]*)"')


@adapter(Interface, IRequest)
@implementer(IFilter)
class CroppingEditorLink(object):

    # important, that our order is before
    # resolveuid_and_caption filter order=800
    # so we can read the scale out of the src attribute
    # XXX: there might be a better approach to do this
    order = 700

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_enabled(self):
        return _checkPermission(ModifyPortalContent, self.context)

    def __call__(self, data):
        img_tags = img_tag.findall(data)
        for tag in img_tags:
            src = src_attr.search(tag).groups(0)
            if len(src) > 0:
                x, uuid, x, field, scale = src[0].split("/")
                img_obj = uuidToObject(uuid)
                if not _checkPermission(ModifyPortalContent, img_obj):
                    continue
                editor_link = \
                    """<a href="resolveuid/%(uid)s/@@croppingeditor?""" \
                    """fieldname=%(field)s&amp;scalename=%(scale)s&amp;""" \
                    """hide_scales=1" class="croppingeditor">%(tag)s</a>""" % \
                    dict(uid=uuid, field=field, scale=scale, tag=tag)
                data = data.replace(tag, editor_link)
        return data
