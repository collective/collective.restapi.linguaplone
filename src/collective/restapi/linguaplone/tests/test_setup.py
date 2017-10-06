# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.restapi.linguaplone.testing import COLLECTIVE_RESTAPI_LINGUAPLONE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.restapi.linguaplone is properly installed."""

    layer = COLLECTIVE_RESTAPI_LINGUAPLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.restapi.linguaplone is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.restapi.linguaplone'))

    def test_browserlayer(self):
        """Test that ICollectiveRestapiLinguaploneLayer is registered."""
        from collective.restapi.linguaplone.interfaces import (
            ICollectiveRestapiLinguaploneLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveRestapiLinguaploneLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_RESTAPI_LINGUAPLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.restapi.linguaplone'])

    def test_product_uninstalled(self):
        """Test if collective.restapi.linguaplone is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.restapi.linguaplone'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveRestapiLinguaploneLayer is removed."""
        from collective.restapi.linguaplone.interfaces import \
            ICollectiveRestapiLinguaploneLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveRestapiLinguaploneLayer, utils.registered_layers())
