from zope.i18nmessageid.message import MessageFactory

from importlib.metadata import PackageNotFoundError
from importlib.metadata import distribution


try:
    distribution("plone.namedfile")
except PackageNotFoundError:
    HAS_NAMEDFILE = False
else:
    HAS_NAMEDFILE = True

# TODO: backwards compatibility (probably not needed)
HAS_DEXTERITY = HAS_NAMEDFILE

imagecroppingMessageFactory = MessageFactory("plone.app.imagecropping")
PRODUCT_NAME = PAI_STORAGE_KEY = "plone.app.imagecropping"
