from zope.i18nmessageid.message import MessageFactory
import pkg_resources

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True

imagecroppingMessageFactory = MessageFactory("plone.app.imagecropping")
PRODUCT_NAME = PAI_STORAGE_KEY = "plone.app.imagecropping"


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
