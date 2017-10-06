# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.restapi.linguaplone


class CollectiveRestapiLinguaploneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.restapi.linguaplone)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.restapi.linguaplone:default')


COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE = CollectiveRestapiLinguaploneLayer()


COLLECTIVE_RESTAPI_LINGUAPLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE,),
    name='CollectiveRestapiLinguaploneLayer:IntegrationTesting'
)


COLLECTIVE_RESTAPI_LINGUAPLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE,),
    name='CollectiveRestapiLinguaploneLayer:FunctionalTesting'
)


COLLECTIVE_RESTAPI_LINGUAPLONE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_RESTAPI_LINGUAPLONE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveRestapiLinguaploneLayer:AcceptanceTesting'
)
