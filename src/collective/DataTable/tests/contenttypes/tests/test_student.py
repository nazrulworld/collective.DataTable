# -*- coding: utf-8 -*-
# ++ This file `test_student.py` is generated at 11/21/15 3:05 PM ++
# Run Test: `bin/test -s collective.DataTable -m contenttypes -t test_student`
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import transaction
from bs4 import BeautifulSoup
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles, login, logout
from plone.testing.z2 import Browser
from zope.component import (queryUtility, createObject)
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import safe_unicode

from collective.DataTable.contenttypes.student import IStudent
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


class TestStudent(unittest.TestCase):

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
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_STUDENT)
        schema = fti.lookupSchema()

        self.assertEquals(schema, IStudent)

    def test_factory(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_STUDENT)

        obj = createObject(fti.factory)

        self.assertTrue(IStudent.providedBy(obj))

    def test_adding(self):
        """
        :return:
        """
        _id = safe_unicode('test-first-name')
        _first_name = safe_unicode('Test First Name')
        _last_name = safe_unicode('Last')

        self.school.invokeFactory(CONTENT_TYPE_STUDENT, _id)
        student = self.school[_id]

        self.assertTrue(IStudent.providedBy(student))

        student.first_name = _first_name
        student.last_name = _last_name

        student.reindexObject()

        result = self.portal.portal_catalog.searchResults(id=student.id)

        self.assertEquals(1, len(result))
        self.assertEqual(_first_name + ' ' + _last_name, result[0].Title)
        self.assertEquals(result[0].getObject().first_name, _first_name)

    def test_globally_add_not_allowed(self):
        """
        :return:
        """

        try:

            self.portal.invokeFactory(CONTENT_TYPE_STUDENT, 'student')

        except ValueError, exc:

            self.assertIn('disallowed', exc.message.lower())
            self.assertIn(CONTENT_TYPE_STUDENT, exc.message)

        else:

            raise AssertionError("This code should not reach here!, Globally not allowed this content type.")


class TestStudentBrowser(unittest.TestCase, CollectiveDataTableBrowserMixin):

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
        _resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        _id = safe_unicode('test-first-name')
        _first_name = safe_unicode('Test First Name')
        _last_name = safe_unicode('Last')
        _gender = safe_unicode('male')
        _roll_number = safe_unicode('1001')
        _grade = safe_unicode('g4')
        _contact_number = safe_unicode('980000000')
        _profile_photo = 'student.jpg'

        _url = self.school.absolute_url() + '/++add++' + CONTENT_TYPE_STUDENT
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
        form.getControl(name='form.widgets.first_name').value = _first_name
        form.getControl(name='form.widgets.last_name').value = _last_name
        form.getControl(name='form.widgets.gender:list').value = (_gender, )
        form.getControl(name='form.widgets.roll_number').value = _roll_number
        form.getControl(name='form.widgets.grade:list').value = (_grade, )
        form.getControl(name='form.widgets.contact_number').value = _contact_number

        form.getControl(name='form.widgets.IShortName.id').value = "test-first-name"
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        image_control = form.getControl(name='form.widgets.profile_photo')
        image_control.add_file(open(os.path.join(_resource_path, _profile_photo), 'rb'), 'image/jpeg', _profile_photo)

        form.submit(form.getControl(name='form.buttons.save').value)

        self.assertEqual(self.school.absolute_url() + '/' + _id + '/view', self.browser.url,
                         'Current URL should be default view for newly created student')
        student = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_STUDENT, id=_id)
        student = student[0]

        self.assertEqual(student.getObject().first_name, _first_name)
        self.assertEqual(student.getObject().gender, _gender)
        self.assertEqual(student.grade, _grade)
        self.assertEqual(student.roll_number, int(_roll_number))
        self.assertEqual(_first_name + ' ' + _last_name, student.Title)

    def test_unique_roll_number(self):

        """
        :return:
        """
        _id = self.school.generateUniqueId(CONTENT_TYPE_STUDENT)
        _first_name = safe_unicode('Test First Name')
        _last_name = safe_unicode('Last')
        _gender = safe_unicode('male')
        _roll_number = safe_unicode('1001')
        _grade = safe_unicode('g4')
        _contact_number = safe_unicode('980000000')

        _url = self.school.absolute_url() + '/++add++' + CONTENT_TYPE_STUDENT
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
        form.getControl(name='form.widgets.first_name').value = _first_name
        form.getControl(name='form.widgets.last_name').value = _last_name
        form.getControl(name='form.widgets.gender:list').value = (_gender, )
        form.getControl(name='form.widgets.roll_number').value = _roll_number
        form.getControl(name='form.widgets.grade:list').value = (_grade, )
        form.getControl(name='form.widgets.contact_number').value = _contact_number

        form.getControl(name='form.widgets.IShortName.id').value = _id
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        form.submit(form.getControl(name='form.buttons.save').value)

        _id = self.school.generateUniqueId(CONTENT_TYPE_STUDENT)
        self.browser.open(_url)
        # Fill the form again
        form = self.browser.getForm(id='form')
        form.getControl(name='form.widgets.first_name').value = _first_name
        form.getControl(name='form.widgets.last_name').value = _last_name
        form.getControl(name='form.widgets.gender:list').value = (_gender, )
        form.getControl(name='form.widgets.roll_number').value = _roll_number
        form.getControl(name='form.widgets.grade:list').value = (_grade, )
        form.getControl(name='form.widgets.contact_number').value = _contact_number

        form.getControl(name='form.widgets.IShortName.id').value = _id
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        form.submit(form.getControl(name='form.buttons.save').value)

        self.assertNotEqual(self.school.absolute_url() + '/' + _id + '/view', self.browser.url,
                            'Current URL should not be default view, as validation error.')

        html_output = BeautifulSoup(self.browser.contents.strip('\n'), 'lxml')
        roll_container = html_output.find('div', id='formfield-form-widgets-roll_number')

        error = roll_container.find('div', class_='fieldErrorBox').find('div', class_='error')

        # We make sure error message shown.
        self.assertIsNotNone(error)
        self.assertTrue(0 < len(error.text))

    def tearDown(self):
        """
        :return:
        """

        error_log = getToolByName(self.portal, 'error_log')

        if len(error_log.getLogEntries()):
            print error_log.getLogEntries()[-1]['tb_text']

        super(TestStudentBrowser, self).tearDown()


def test_suite():
    """
    :return:
    """
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestStudent, prefix='test'))
    suite.addTest(unittest.makeSuite(TestStudentBrowser, prefix='test'))

    return suite
