from plone.app.imagecropping.interfaces import ICroppingInfoChangedEvent
from plone.app.imagecropping.interfaces import ICroppingInfoRemovedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class CroppingInfoChangedEvent(ObjectEvent):
    """ """
    implements(ICroppingInfoChangedEvent)


class CroppingInfoRemovedEvent(ObjectEvent):
    """ """
    implements(ICroppingInfoRemovedEvent)
