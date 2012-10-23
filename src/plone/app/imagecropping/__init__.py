from zope.i18nmessageid.message import MessageFactory


imagecroppingMessageFactory = MessageFactory("plone.app.imagecropping")
PAI_STORAGE_KEY = "plone.app.imagecropping"


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
