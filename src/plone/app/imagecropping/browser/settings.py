from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper, \
    RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface.interface import Interface


class ISettings(Interface):
    """ Define settings data structure """

    large_size = schema.TextLine(
        title=u"Crop Editor Large Size",
        required=False,
        default=u"1000:1000",
    )

    min_size = schema.TextLine(
        title=u"Minimum Crop Area Size",
        required=False,
        default=u"10:10"
    )


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = ISettings
    label = u"plone.app.imagecropping Settings"


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
