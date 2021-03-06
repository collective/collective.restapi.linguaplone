# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone.interfaces import ITranslatable
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import providedBy

import plone.protect.interfaces
import six


@implementer(IExpandableElement)
@adapter(ITranslatable, Interface)
class Translations(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "translations": {
                "@id": "{}/@translations".format(self.context.absolute_url())
            }
        }
        if not expand:
            return result

        translations = []
        for language, translation in self.context.getTranslations(
            review_state=False
        ).items():
            if language != self.context.Language():
                translations.append(
                    {"@id": translation.absolute_url(), "language": language}
                )

        result["translations"]["items"] = translations
        return result


class TranslationInfo(Service):
    """ Get translation information
    """

    def reply(self):
        translations = Translations(self.context, self.request)
        return translations(expand=True)["translations"]


class LinkTranslations(Service):
    """ Link two content objects as translations of each other
    """

    def __init__(self, context, request):
        super(LinkTranslations, self).__init__(context, request)
        self.portal = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state"
        ).portal()
        self.portal_url = self.portal.absolute_url()
        self.catalog = getToolByName(self.context, "portal_catalog")

    def reply(self):
        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        data = json_body(self.request)
        id_ = data.get("id", None)
        if id_ is None:
            self.request.response.setStatus(400)
            return dict(
                error=dict(type="BadRequest", message="Missing content id to link to")
            )

        target = self.get_object(id_)
        if target is None:
            self.request.response.setStatus(400)
            return dict(error=dict(type="BadRequest", message="Content does not exist"))

        target_language = target.Language()
        if self.context.hasTranslation(target_language):
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="Already translated into language {}".format(
                        target_language
                    ),
                )
            )

        self.context.addTranslationReference(target)
        self.request.response.setStatus(201)
        self.request.response.setHeader("Location", self.context.absolute_url())
        return {}

    def get_object(self, key):
        if isinstance(key, six.string_types):
            if key.startswith(self.portal_url):
                # Resolve by URL
                key = key[len(self.portal_url) + 1 :]
                if six.PY2:
                    key = key.encode("utf8")
                return self.portal.restrictedTraverse(key, None)
            elif key.startswith("/"):
                if six.PY2:
                    key = key.encode("utf8")
                # Resolve by path
                return self.portal.restrictedTraverse(key.lstrip("/"), None)
            else:
                # Resolve by UID
                brain = self.catalog(UID=key)
                if brain:
                    return brain[0].getObject()


class UnlinkTranslations(Service):
    """ Unlink the translations for a content object
    """

    def reply(self):
        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        data = json_body(self.request)
        language = data.get("language", None)
        if language is None:
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="You need to provide the language to unlink",
                )
            )

        if not self.context.hasTranslation(language):
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="This object is not translated into {}".format(language),
                )
            )

        self.context.removeTranslation(language)
        self.request.response.setStatus(204)
        return {}
