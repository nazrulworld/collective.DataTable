# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_ID, setRoles
from plone.registry.interfaces import IRegistry
from zope.component import getAdapter
from zope.component import getUtility

from collective.DataTable.interfaces import IConfiguration
from collective.DataTable.testing import COLLECTIVE_DATATABLE_INTEGRATION_TESTING


class SearchControlPanelAdapterTest(unittest.TestCase):

    layer = COLLECTIVE_DATATABLE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        registry = getUtility(IRegistry)
        self.configurations = registry.forInterface(
            IConfiguration, prefix="collective.DataTable")

    def test_adapter_lookup(self):
        self.assertTrue(getAdapter(self.portal, IConfiguration))

    def _test_get_enable_livesearch(self):
        self.assertEqual(
            getAdapter(self.portal, IConfiguration).enable_livesearch,
            True
        )
        self.configurations.enable_livesearch = False
        self.assertEquals(
            getAdapter(self.portal, IConfiguration).enable_livesearch,
            False
        )

    def _test_set_enable_livesearch(self):
        self.assertEquals(
            self.configurations.enable_livesearch,
            True
        )
        getAdapter(self.portal, IConfiguration).enable_livesearch = False
        self.assertEquals(
            self.configurations.enable_livesearch,
            False
        )

    def _test_get_types_not_searched(self):
        self.assertTrue(
            'Folder' not in
            getAdapter(self.portal, IConfiguration).types_not_searched
        )
        self.search_settings.types_not_searched = ('Folder',)
        self.assertTrue(
            'Folder' in
            getAdapter(self.portal, IConfiguration).types_not_searched
        )

    def _test_set_types_not_searched(self):
        self.assertTrue(
            'Folder' not in self.configurations.types_not_searched
        )
        getAdapter(self.portal, IConfiguration).types_not_searched = ('Folder',)
        self.assertTrue(
            'Folder' in self.configurations.types_not_searched
        )
