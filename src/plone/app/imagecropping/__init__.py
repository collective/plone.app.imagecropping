# -*- coding: utf-8 -*-
from zope.i18nmessageid.message import MessageFactory

import pkg_resources


try:
    pkg_resources.get_distribution('plone.namedfile')
except pkg_resources.DistributionNotFound:
    HAS_NAMEDFILE = False
else:
    HAS_NAMEDFILE = True

# TODO: backwards compatibility (probably not needed)
HAS_DEXTERITY = HAS_NAMEDFILE

imagecroppingMessageFactory = MessageFactory('plone.app.imagecropping')
PRODUCT_NAME = PAI_STORAGE_KEY = 'plone.app.imagecropping'
