from collective.restapi.linguaplone.testing import COLLECTIVE_RESTAPI_LINGUAPLONE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.utils import createContentInContainer
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.expansion import expandable_elements
from plone.restapi.testing import RelativeSession
from zope.component import getMultiAdapter
from zope.component import provideAdapter
from zope.interface import Interface
from zope.interface import providedBy
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserRequest

import unittest
import transaction


class TestExpansionFunctional(unittest.TestCase):

    layer = COLLECTIVE_RESTAPI_LINGUAPLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.request = self.layer['request']
        # self.portal.portal_languages.addSupportedLanguage('en')
        # self.portal.portal_languages.addSupportedLanguage('es')
        #  Setup the language root folders
        login(self.portal, SITE_OWNER_NAME)
        lsf = getMultiAdapter(
            (self.portal, self.request),
            name='language-setup-folders'
        )
        lsf()

        en_id = self.portal.en.invokeFactory(
            id='test-document',
            type_name='Document',
            title='Test document'
        )
        self.en_content = self.portal.en.get(en_id)

        es_id = self.portal.es.invokeFactory(
            id='test-document',
            type_name='Document',
            title='Test document'
        )
        self.es_content = self.portal.es.get(es_id)
        self.en_content.addTranslationReference(self.es_content)

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        transaction.commit()

    def test_translations_is_expandable(self):
        response = self.api_session.get('/en/test-document')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'translations',
            response.json().get('@components').keys()
        )

    def test_translations_expanded(self):
        response = self.api_session.get(
            '/en/test-document',
            params={
                "expand": "translations"
            }
        )

        self.assertEqual(response.status_code, 200)
        translation_dict = {
            '@id': self.es_content.absolute_url(),
            'language': 'es'
        }
        self.assertIn(
            translation_dict,
            response.json()['@components']['translations']['items']
        )
