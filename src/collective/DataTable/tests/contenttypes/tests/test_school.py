# -*- coding: utf-8 -*-
# ++ This file `test_school.py` is generated at 11/12/15 4:40 PM ++
# Run Test: `bin/test -s collective.DataTable -m contenttypes -t test_school`
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from Products.CMFCore.utils import getToolByName

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles, login, logout
from plone.testing.z2 import Browser
from zope.component import (queryUtility, createObject)
from plone.dexterity.interfaces import IDexterityFTI

from collective.DataTable.contenttypes.school import ISchool
from collective.DataTable.testing import (COLLECTIVE_DATATABLE_INTEGRATION_TESTING,
                                          COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING)
from collective.DataTable.testing import CollectiveDataTableBrowserMixin

CONTENT_TYPE_SCHOOL = 'collective.DataTable.School'
CONTENT_TYPE_BOOK = 'collective.DataTable.Book'
CONTENT_TYPE_LIBRARY = 'collective.DataTable.Library'
CONTENT_TYPE_STUDENT = 'collective.DataTable.Student'

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


class TestSchool(unittest.TestCase):

    """
    """
    layer = COLLECTIVE_DATATABLE_INTEGRATION_TESTING

    def setUp(self):
        """
        :return:
        """
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])

        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_SCHOOL)
        schema = fti.lookupSchema()

        self.assertEquals(schema, ISchool)

    def test_factory(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_SCHOOL)

        obj = createObject(fti.factory)

        self.assertTrue(ISchool.providedBy(obj))

    def test_adding(self):
        """
        :return:
        """
        self.portal.invokeFactory(CONTENT_TYPE_SCHOOL, 'school')
        school = self.portal['school']

        self.assertTrue(ISchool.providedBy(school))
        school.setTitle('My Test School')

        school.reindexObject()

        result = self.portal.portal_catalog.searchResults(id=school.id)

        self.assertEquals(1, len(result))

        self.assertEquals(result[0].Title, 'My Test School')

    def test_allow_add_student_and_library_types(self):

        """
        :return:
        """
        self.portal.invokeFactory(CONTENT_TYPE_SCHOOL, 'school')
        school = self.portal['school']
        school.setTitle('My Test School')

        school.reindexObject()

        # we make sure, other than school and library type allowed, should raise ValueError exception
        try:
            school.invokeFactory(CONTENT_TYPE_BOOK, 'new-book')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIn('disallowed', _msg)
        self.assertIn(CONTENT_TYPE_BOOK, _msg)

        # Make sure Library type allowed
        try:
            school.invokeFactory(CONTENT_TYPE_LIBRARY, 'new-library')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIsNone(_msg)

        # Make sure Student type allowed
        try:
            school.invokeFactory(CONTENT_TYPE_STUDENT, 'new-student')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIsNone(_msg)


class TestSchoolBrowser(unittest.TestCase, CollectiveDataTableBrowserMixin):

    """
    """
    layer = COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING

    def setUp(self):
        """
        :return:
        """
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])

        self.installer = api.portal.get_tool('portal_quickinstaller')

        self.browser = Browser(self.layer['app'])

    def test_adding_by_browser(self):

        """
        :return:
        """
        _resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

        _url = self.portal.absolute_url() + '/++add++' + CONTENT_TYPE_SCHOOL
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
        form.getControl(name='form.widgets.title').value = 'New Test School'
        form.getControl(name='form.widgets.description').value = "<b>Test description for this school</b>"
        form.getControl(name='form.widgets.IShortName.id').value = "test-school-url"
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        image_control = form.getControl(name='form.widgets.feature_photo')
        image_control.add_file(open(os.path.join(_resource_path, 'school-building.png'), 'rb'),
                               'image/png',
                               'school-building.png')

        form.submit(form.getControl(name='form.buttons.save').value)

        self.assertEqual(self.portal.absolute_url() + '/test-school-url/view', self.browser.url,
                         'Current URL should be default view for newly created school')
        school = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_SCHOOL, id='test-school-url')
        school = school[0]

        self.assertEqual(school.Title, 'New Test School')
        self.assertEqual(school.getObject().feature_photo.filename, 'school-building.png')

    def test_form_validation(self):
        """
        :return:
        """
        _url = self.portal.absolute_url() + '/++add++' + CONTENT_TYPE_SCHOOL
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
        # form.getControl(name='form.widgets.title').value = 'New Test School'
        # form.getControl(name='form.widgets.description').value = "<b>Test description for this school</b>"

        form.getControl(name='form.widgets.title').value = ''
        form.getControl(name='form.widgets.description').value = ''

        form.submit(form.getControl(name='form.buttons.save').value)
        self.assertEqual(_url, self.browser.url, 'Current URL should be as school creation url')

        school = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_SCHOOL)

        self.assertEqual(0, len(school))

        form = self.browser.getForm(id='form')
        form.getControl(name='form.widgets.title').value = ''
        form.getControl(name='form.widgets.description').value = '<b>Test description for this school</b'

        form.submit(form.getControl(name='form.buttons.save').value)
        self.assertEqual(_url, self.browser.url, 'Current URL should be as school creation url')

        school = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_SCHOOL)

        self.assertEqual(0, len(school))

    def tearDown(self):
        """
        :return:
        """

        error_log = getToolByName(self.portal, 'error_log')

        if len(error_log.getLogEntries()):
            print error_log.getLogEntries()[-1]['tb_text']

        super(TestSchoolBrowser, self).tearDown()

def test_suite():
    """
    :return:
    """
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestSchool, prefix='test'))
    suite.addTest(unittest.makeSuite(TestSchoolBrowser, prefix='test'))

    return suite
