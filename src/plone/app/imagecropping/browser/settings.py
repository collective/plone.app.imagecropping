from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper, \
    RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface.interface import Interface
from plone.app.imagecropping import imagecroppingMessageFactory as _


class ISettings(Interface):
    """ Define settings data structure """

    large_size = schema.TextLine(
        title=_(u"Crop Editor Large Size"),
        description=_(u"width:height"),
        required=False,
        default=u"1000:1000",
    )

    min_size = schema.TextLine(
        title=_(u"Minimum Crop Area Size"),
        description=_(u"width:height"),
        required=False,
        default=u"10:10"
    )


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = ISettings
    label = _(u"Image Cropping Settings")


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
