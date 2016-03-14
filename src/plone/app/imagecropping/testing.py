# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2


class PloneAppImagecropping(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.imagecropping
        self.loadZCML('testing.zcml', package=plone.app.imagecropping)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.imagecropping:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.portal_workflow.setDefaultChain('one_state_workflow')
        portal.invokeFactory(
            'Folder',
            id='acceptance-test-folder',
            title=u'Test Folder'
        )


IMAGECROPPING = PloneAppImagecropping()
IMAGECROPPING_INTEGRATION = IntegrationTesting(
    bases=(IMAGECROPPING, ),
    name='plone.app.imagecropping:Integration'
)
IMAGECROPPING_FUNCTIONAL = FunctionalTesting(
    bases=(IMAGECROPPING, ),
    name='plone.app.imagecropping:Functional')
IMAGECROPPING_ROBOT = FunctionalTesting(
    bases=(
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        IMAGECROPPING,
        z2.ZSERVER_FIXTURE
    ),
    name='plone.app.imagecropping:Robot'
)
