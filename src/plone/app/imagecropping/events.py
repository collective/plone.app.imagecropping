# -*- coding: utf-8 -*-
from plone.app.imagecropping.interfaces import ICroppingInfoChangedEvent
from plone.app.imagecropping.interfaces import ICroppingInfoRemovedEvent
from zope.interface.interfaces import ObjectEvent
from zope.interface import implementer


@implementer(ICroppingInfoChangedEvent)
class CroppingInfoChangedEvent(ObjectEvent):
    """ """


@implementer(ICroppingInfoRemovedEvent)
class CroppingInfoRemovedEvent(ObjectEvent):
    """ """
