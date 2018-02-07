# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing import z2

import collective.restapi.linguaplone


class CollectiveRestapiLinguaploneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import Products.LinguaPlone
        import plone.restapi
        self.loadZCML(package=Products.LinguaPlone)
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.restapi.linguaplone)

        z2.installProduct(app, 'Products.Archetypes')
        z2.installProduct(app, 'Products.ATContentTypes')
        z2.installProduct(app, 'Products.LinguaPlone')
        z2.installProduct(app, 'plone.app.collection')
        z2.installProduct(app, 'plone.app.blob')
        z2.installProduct(app, 'plone.restapi')

    def setUpPloneSite(self, portal):

        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ['Manager'], [])

        login(portal, SITE_OWNER_NAME)

        if portal.portal_setup.profileExists(
                'Products.ATContentTypes:default'):
            applyProfile(portal, 'Products.ATContentTypes:default')
        if portal.portal_setup.profileExists(
                'plone.app.collection:default'):
            applyProfile(portal, 'plone.app.collection:default')

        applyProfile(portal, 'Products.LinguaPlone:LinguaPlone')
        applyProfile(portal, 'plone.restapi:default')

        portal.portal_languages.addSupportedLanguage('en')
        portal.portal_languages.addSupportedLanguage('es')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")


COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE = CollectiveRestapiLinguaploneLayer()


COLLECTIVE_RESTAPI_LINGUAPLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE,),
    name='CollectiveRestapiLinguaploneLayer:IntegrationTesting'
)


COLLECTIVE_RESTAPI_LINGUAPLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectiveRestapiLinguaploneLayer:FunctionalTesting'
)
