.. _translations:

LinguaPlone Translations
========================

.. note::
    This addon will only work with `Products.LinguaPlone`_ in Plone 4.
    You can install `collective.restapi.pam`_ if you want to get similar
    features in Plone 4 using `plone.app.multilingual`_ versions 1.x and 2.x
    and use plain `plone.restapi`_ in Plone 5.

Using this addon you can get information about the translations of a content
object handled using `Products.LinguaPlone`_. To achieve that it provides a
`@translations` endpoint to handle the translation information of the content
objects.

Once we have installed `Products.LinguaPlone`_ and enabled more than one
language we can link two content-items of different languages to be the
translation of each other issuing a `POST` query to the `@translations`
endpoint including the `id` of the content which should be linked to. The
`id` of the content must be a full URL of the content object:


..  http:example:: curl httpie python-requests
    :request: _json/translations_post.req


.. note::
    "id" is a required field and needs to point to an existing content on the site.

The API will return a `201 Created` response if the linking was successful.


.. literalinclude:: _json/translations_post.resp
   :language: http


We can also use the object's path to link the translation instead of the full URL:

..  http:example:: curl httpie python-requests
    :request: _json/translations_post_by_id.req

.. literalinclude:: _json/translations_post_by_id.resp
   :language: http


We can also use the object's UID to link the translation:

..  http:example:: curl httpie python-requests
    :request: _json/translations_post_by_uid.req

.. literalinclude:: _json/translations_post_by_id.resp
   :language: http




After linking the contents we can get the list of the translations of that
content item by issuing a ``GET`` request on the `@translations` endpoint of
that content item.:

..  http:example:: curl httpie python-requests
    :request: _json/translations_get.req

.. literalinclude:: _json/translations_get.resp
   :language: http


To unlink the content, issue a ``DELETE`` request on the `@translations`
endpoint of the content item and provide the language code you want to unlink.:


..  http:example:: curl httpie python-requests
    :request: _json/translations_delete.req

.. note::
    "language" is a required field.

.. literalinclude:: _json/translations_delete.resp
   :language: http


Expansion
---------

This endpoint uses the `expansion`_ mechanism of `plone.restapi`_ which allows to get additional
information about a content item in one query, avoiding unnecesary requests.

If a simple ``GET`` request is done on the content item, a new entry will be shown on the `@components`
entry with the URL of the `@translations` endpoint:

..  http:example:: curl httpie python-requests
    :request: _json/translations_is_expandable.req

.. literalinclude:: _json/translations_is_expandable.resp
   :language: http


That means that, to include the translations of the item in the main content response, you can
request to expand it:

..  http:example:: curl httpie python-requests
    :request: _json/expand_translations.req

And the response will include the required information:

.. literalinclude:: _json/expand_translations.resp
   :language: http



.. _`Products.LinguaPlone`: https://pypi.python.org/pypi/Products.LinguaPlone
.. _`collective.restapi.pam`: https://pypi.python.org/pypi/collective.restapi.pam
.. _`plone.app.multilingual`: https://pypi.python.org/pypi/plone.app.multilingual
.. _`plone.restapi`: https://pypi.python.org/pypi/plone.restapi
.. _`expansion`: https://plonerestapi.readthedocs.io/en/latest/expansion.html
