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


.. _`Products.LinguaPlone`: https://pypi.python.org/pypi/Products.LinguaPlone
.. _`collective.restapi.pam`: https://pypi.python.org/pypi/collective.restapi.pam
.. _`plone.app.multilingual`: https://pypi.python.org/pypi/plone.app.multilingual
.. _`plone.restapi`: https://pypi.python.org/pypi/plone.restapi
