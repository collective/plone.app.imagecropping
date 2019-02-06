# -*- coding: utf-8 -*-
from plone.app.imagecropping import imagecroppingMessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.namedfile.interfaces import IAvailableSizes
from plone.z3cform import layout
from z3c.form import form
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SizesVocabulary(object):

    def __call__(self, context):
        allowed_sizes = getUtility(IAvailableSizes)()
        size_names = allowed_sizes and list(allowed_sizes.keys()) or []
        return SimpleVocabulary.fromValues(size_names)


class ISettings(Interface):
    ' Define settings data structure '

    constrain_cropping = schema.Bool(
        title=_(u'Enable to constrain croppable scales'),
        description=_(u'Enable to reduce the scales shown for cropping in the '
                      u'list of scales with crop support.'),
        default=False,
        required=False,
    )

    cropping_for = schema.List(
        title=_(u'List of scales with crop support'),
        description=_(u'Select the scales with cropping support enabled. Only '
                      u'active if enabled with checkbox.'),
        required=False,
        default=[],
        value_type=schema.Choice(
            vocabulary='plone.app.imagecropping.all_sizes'),
    )

    """XXX: not implemented right now
    auto_cropping_for = schema.List(
        title=_(u'Scales with auto crop'),
        description=_(u'Scales to be auto cropped in center of image.'),
        required=False,
        default=[],
        value_type=Choice(
            vocabulary='plone.app.imagecropping.all_sizes'),
    )
    """


class SettingsEditForm(RegistryEditForm):
    """ Define form logic
    """
    form.extends(RegistryEditForm)
    schema = ISettings
    label = _(u'Image Cropping Settings')


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
