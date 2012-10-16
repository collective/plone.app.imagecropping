from plone.app.testing import FunctionalTesting, IntegrationTesting, \
    PloneWithPackageLayer
import plone.app.imagecropping


PLONE_APP_IMAGECROPPING = PloneWithPackageLayer(
    zcml_package=plone.app.imagecropping,
    zcml_filename='testing.zcml',
    gs_profile_id='plone.app.imagecropping:testing',
    name="PLONE_APP_IMAGECROPPING")

PLONE_APP_IMAGECROPPING_INTEGRATION = IntegrationTesting(
    bases=(PLONE_APP_IMAGECROPPING, ),
    name="PLONE_APP_IMAGECROPPING_INTEGRATION")

PLONE_APP_IMAGECROPPING_FUNCTIONAL = FunctionalTesting(
    bases=(PLONE_APP_IMAGECROPPING, ),
    name="PLONE_APP_IMAGECROPPING_FUNCTIONAL")
