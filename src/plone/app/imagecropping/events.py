from plone.app.imagecropping.interfaces import ICroppingInfoChangedEvent
from plone.app.imagecropping.interfaces import ICroppingInfoRemovedEvent
from zope.interface import implementer
from zope.interface.interfaces import ObjectEvent


@implementer(ICroppingInfoChangedEvent)
class CroppingInfoChangedEvent(ObjectEvent):
    """ """


@implementer(ICroppingInfoRemovedEvent)
class CroppingInfoRemovedEvent(ObjectEvent):
    """ """
