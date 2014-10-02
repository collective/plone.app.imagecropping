# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2

import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY_CONTENTTYPES = False
else:
    HAS_DEXTERITY_CONTENTTYPES = True


class PloneAppImagecropping(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.imagecropping
        self.loadZCML('testing.zcml', package=plone.app.imagecropping)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.imagecropping:testing')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain('one_state_workflow')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory(
            'Folder',
            id='acceptance-test-folder',
            title=u'Test Folder'
        )


class PloneAppImagecroppingDX(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'Products.DateRecurringIndex')
        if HAS_DEXTERITY_CONTENTTYPES:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)

        import plone.app.imagecropping
        self.loadZCML('testing.zcml', package=plone.app.imagecropping)

    def setUpPloneSite(self, portal):
        if HAS_DEXTERITY_CONTENTTYPES:
            applyProfile(portal, 'plone.app.contenttypes:default')

        applyProfile(portal, 'plone.app.imagecropping:testing')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain('one_state_workflow')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory(
            'Folder',
            id='acceptance-test-folder',
            title=u'Test Folder'
        )


PLONE_APP_IMAGECROPPING = PloneAppImagecropping()
PLONE_APP_IMAGECROPPING_INTEGRATION = IntegrationTesting(
    bases=(PLONE_APP_IMAGECROPPING, ),
    name='plone.app.imagecropping:Integration')
PLONE_APP_IMAGECROPPING_FUNCTIONAL = FunctionalTesting(
    bases=(PLONE_APP_IMAGECROPPING, ),
    name='plone.app.imagecropping:Functional')
PLONE_APP_IMAGECROPPING_DX = PloneAppImagecroppingDX()
PLONE_APP_IMAGECROPPING_INTEGRATION_DX = IntegrationTesting(
    bases=(PLONE_APP_IMAGECROPPING_DX, ),
    name='plone.app.imagecropping:Integration_DX')
PLONE_APP_IMAGECROPPING_FUNCTIONAL_DX = FunctionalTesting(
    bases=(PLONE_APP_IMAGECROPPING_DX, ),
    name='plone.app.imagecropping:Functional_DX')
PLONE_APP_IMAGECROPPING_ROBOT = FunctionalTesting(
    bases=(
        AUTOLOGIN_LIBRARY_FIXTURE,
        PLONE_APP_IMAGECROPPING,
        z2.ZSERVER_FIXTURE
    ),
    name='plone.app.imagecropping:Robot')
