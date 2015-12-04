# -*- coding: utf-8 -*-
# ++ This file `test_library.py` is generated at 11/21/15 12:06 PM ++
# Run Test: `bin/test -s collective.DataTable -m contenttypes -t test_library`
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import transaction
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles, login, logout
from plone.testing.z2 import Browser
from zope.component import (queryUtility, createObject)
from plone.dexterity.interfaces import IDexterityFTI

from collective.DataTable.contenttypes.library import ILibrary
from collective.DataTable.testing import (COLLECTIVE_DATATABLE_INTEGRATION_TESTING,
                                          COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING)
from collective.DataTable.testing import CollectiveDataTableBrowserMixin
from collective.DataTable.testing import (
    CONTENT_TYPE_SCHOOL,
    CONTENT_TYPE_BOOK,
    CONTENT_TYPE_LIBRARY,
    CONTENT_TYPE_STUDENT)

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


def init_fixture(self, commit=False):

    """
    :param self:
    :param commit:
    :return:
    """
    self.portal.invokeFactory(CONTENT_TYPE_SCHOOL, 'school')
    self.school = self.portal['school']
    self.school.setTitle('My Test School')
    self.school.reindexObject()

    if commit:
        transaction.commit()


class TestLibrary(unittest.TestCase):

    """
    """
    layer = COLLECTIVE_DATATABLE_INTEGRATION_TESTING

    def setUp(self):
        """
        :return:
        """
        self.school = None

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        init_fixture(self)

    def test_schema(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_LIBRARY)
        schema = fti.lookupSchema()

        self.assertEquals(schema, ILibrary)

    def test_factory(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_LIBRARY)

        obj = createObject(fti.factory)

        self.assertTrue(ILibrary.providedBy(obj))

    def test_adding(self):
        """
        :return:
        """
        self.school.invokeFactory(CONTENT_TYPE_LIBRARY, 'library')
        library = self.school['library']

        self.assertTrue(ILibrary.providedBy(library))
        library.setTitle('My Test Library')
        library.setDescription('The test library for test school.')

        library.reindexObject()

        result = self.portal.portal_catalog.searchResults(id=library.id)

        self.assertEquals(1, len(result))

        self.assertEquals(result[0].Title, 'My Test Library')

    def test_allow_add_book_type_only(self):

        """
        :return:
        """
        self.school.invokeFactory(CONTENT_TYPE_LIBRARY, 'library')
        library = self.school['library']
        library.setTitle('My Test Library')

        library.reindexObject()

        # we make sure, other than school and library type allowed, should raise ValueError exception
        try:
            library.invokeFactory(CONTENT_TYPE_STUDENT, 'new-student')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIn('disallowed', _msg)
        self.assertIn(CONTENT_TYPE_STUDENT, _msg)

        # Make sure Book type allowed
        try:
            library.invokeFactory(CONTENT_TYPE_BOOK, 'new-book')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIsNone(_msg)

    def test_globally_add_not_allowed(self):
        """
        :return:
        """

        try:

            self.portal.invokeFactory(CONTENT_TYPE_LIBRARY, 'library')

        except ValueError, exc:

            self.assertIn('disallowed', exc.message.lower())
            self.assertIn(CONTENT_TYPE_LIBRARY, exc.message)

        else:

            raise AssertionError("This could should nor reach here!, Globally not allowed this content type.")


class TestLibraryBrowser(unittest.TestCase, CollectiveDataTableBrowserMixin):

    """
    """
    layer = COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING

    def setUp(self):
        """
        :return:
        """
        self.school = None

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        init_fixture(self, True)

        self.browser = Browser(self.layer['app'])

    def test_adding_by_browser(self):

        """
        :return:
        """

        _url = self.school.absolute_url() + '/++add++' + CONTENT_TYPE_LIBRARY
        self.browser.open(_url)

        try:
            form = self.browser.getForm(id='form')

        except LookupError as exc:

            if not self.browser.cookies.get('__ac', None):

                self.browser_login()
                form = self.browser.getForm(id='form')
            else:
                raise LookupError(exc.message)

        # Fill the form
        form.getControl(name='form.widgets.title').value = 'New Test Library'
        form.getControl(name='form.widgets.description').value = "<b>Test description for this library</b>"
        form.getControl(name='form.widgets.IShortName.id').value = "test-library-url"
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        form.submit(form.getControl(name='form.buttons.save').value)

        self.assertEqual(self.school.absolute_url() + '/test-library-url/view', self.browser.url,
                         'Current URL should be default view for newly created library')
        library = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_LIBRARY, id='test-library-url')
        library = library[0]

        self.assertEqual(library.Title, 'New Test Library')

    def tearDown(self):
        """
        :return:
        """

        error_log = getToolByName(self.portal, 'error_log')

        if len(error_log.getLogEntries()):
            print error_log.getLogEntries()[-1]['tb_text']

        super(TestLibraryBrowser, self).tearDown()
