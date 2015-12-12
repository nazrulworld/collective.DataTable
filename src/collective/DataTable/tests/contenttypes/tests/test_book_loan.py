# -*- coding: utf-8 -*-
# ++ This file `test_book.py` is generated at 11/30/15 6:38 PM ++
# Run Test: `bin/test -s collective.DataTable -m contenttypes -t test_book_review`
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import transaction
from bs4 import BeautifulSoup
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles, login, logout
from plone.testing.z2 import Browser
from zope.component import (queryUtility, createObject)
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import safe_unicode

from collective.DataTable.contenttypes.book_loan import IBookLoan
from collective.DataTable.testing import (COLLECTIVE_DATATABLE_INTEGRATION_TESTING,
                                          COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING)
from collective.DataTable.testing import CollectiveDataTableBrowserMixin
from collective.DataTable.constrains import (
    CONTENT_TYPE_SCHOOL,
    CONTENT_TYPE_BOOK,
    CONTENT_TYPE_LIBRARY,
    CONTENT_TYPE_STUDENT,
    CONTENT_TYPE_BOOK_LOAN,
    CONTENT_TYPE_BOOK_REVIEW,
)

from collective.DataTable.events import collective_datatable_book_loan_created

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

    self.school.invokeFactory(CONTENT_TYPE_STUDENT, 'student')
    self.student = self.school['student']

    self.student.first_name = safe_unicode('Test First Name')
    self.student.last_name = safe_unicode('Last')
    self.student.gender = safe_unicode('male')
    self.student.roll_number = safe_unicode('1001')
    self.student.grade = safe_unicode('g4')
    self.student.contact_number = safe_unicode('980000000')

    self.school.invokeFactory(CONTENT_TYPE_LIBRARY, 'library')
    self.library = self.school['library']
    self.library.setTitle('My Test Library')

    self.school.reindexObject()

    if commit:
        transaction.commit()


class TestBookLoan(unittest.TestCase):

    """
    """
    layer = COLLECTIVE_DATATABLE_INTEGRATION_TESTING

    def setUp(self):
        """
        :return:
        """
        self.school = None
        self.library = None
        self.student = None
        self.book = None

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        init_fixture(self)
        self._book_structure()

    def _book_structure(self):
        """
        :return:
        """
        self.library.invokeFactory(CONTENT_TYPE_BOOK, 'book')
        self.book = self.library['book']
        self.book.setTitle('My Test Book')

        self.book.details = safe_unicode('<h1>Test Book Details</h1>')
        self.book.isbn = safe_unicode('98-999-99-9999')
        self.book.author = safe_unicode('Test Author')
        self.book.publisher = safe_unicode('Test Publisher')
        self.book.number_of_copy = safe_unicode('2')

    def test_schema(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_BOOK_LOAN)
        schema = fti.lookupSchema()

        self.assertEquals(schema, IBookLoan)

    def test_factory(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_BOOK_LOAN)

        obj = createObject(fti.factory)

        self.assertTrue(IBookLoan.providedBy(obj))

    def test_adding(self):
        """
        :return:
        """
        _id = self.book.generateUniqueId(CONTENT_TYPE_BOOK_LOAN)

        intids = getUtility(IIntIds)

        _book = RelationValue(intids.getId(self.book))
        _student = RelationValue(intids.getId(self.student))
        _loan_duration = safe_unicode('2')
        _loan_status = safe_unicode('running')

        self.book.invokeFactory(CONTENT_TYPE_BOOK_LOAN, _id)
        loan = self.book[_id]

        self.assertTrue(IBookLoan.providedBy(loan))

        loan.student = _student
        loan.book = _book
        loan.loan_duration = _loan_duration
        loan.loan_status = _loan_status
        loan.reindexObject()

        # Let's manually triggers
        collective_datatable_book_loan_created(loan, None)

        result = self.portal.portal_catalog.searchResults(id=loan.id)

        self.assertEquals(1, len(result))
        self.assertEqual(self.book, loan.book.to_object)
        self.assertEqual(self.student, loan.student.to_object)
        # Make sure events fired
        self.assertFalse(loan.is_lock)
        self.assertEqual(self.book.number_of_loan_copy, 2)

    def test_globally_add_not_allowed(self):
        """
        :return:
        """

        try:

            self.portal.invokeFactory(CONTENT_TYPE_BOOK_LOAN, 'book_loan')

        except ValueError, exc:

            self.assertIn('disallowed', exc.message.lower())
            self.assertIn(CONTENT_TYPE_BOOK_LOAN, exc.message)

        else:

            raise AssertionError("This code should not reach here!, Globally not allowed this content type.")

    def test_book_stock_validator(self):
        """
        :return:
        """
        pass


class TestBookLoanBrowser(unittest.TestCase, CollectiveDataTableBrowserMixin):

    """
    """
    layer = COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING

    def setUp(self):
        """
        :return:
        """
        self.school = None
        self.student = None
        self.library = None
        self.book = None

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        init_fixture(self, True)
        self.browser = Browser(self.layer['app'])

        self._book_structure()

    def _book_structure(self):
        """
        :return:
        """
        _resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        _id = safe_unicode('book')
        _title = safe_unicode('Test First Book')
        _description = safe_unicode('The test description')
        _details = safe_unicode('<h1>Test Book Details</h1>')
        _isbn = safe_unicode('ISBN 978-0-306-40615-7')
        _author = safe_unicode('Test Author')
        _publisher = safe_unicode('Test Publisher')
        _number_of_copy = safe_unicode('2')
        _cover_photo = 'book.jpg'

        _url = self.library.absolute_url() + '/++add++' + CONTENT_TYPE_BOOK
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
        form.getControl(name='form.widgets.title').value = _title
        form.getControl(name='form.widgets.description').value = _description
        form.getControl(name='form.widgets.isbn').value = _isbn
        form.getControl(name='form.widgets.details').value = _details
        form.getControl(name='form.widgets.publisher').value = _publisher
        form.getControl(name='form.widgets.author').value = _author
        form.getControl(name='form.widgets.number_of_copy').value = _number_of_copy

        form.getControl(name='form.widgets.IShortName.id').value = _id
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        image_control = form.getControl(name='form.widgets.cover_photo')
        image_control.add_file(open(os.path.join(_resource_path, _cover_photo), 'rb'), 'image/jpeg', _cover_photo)

        form.submit(form.getControl(name='form.buttons.save').value)

        book = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_BOOK, id=_id)[0]
        self.book = book.getObject()

    def test_adding_by_browser(self):

        """
        :return:
        """
        _id = self.book.generateUniqueId(CONTENT_TYPE_BOOK_LOAN).replace('.', '-')

        _url = self.book.absolute_url() + '/++add++' + CONTENT_TYPE_BOOK_LOAN
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

        form.getControl(name='form.widgets.book').value = self.book.UID()
        form.getControl(name='form.widgets.student').value = self.student.UID()
        form.getControl(name='form.widgets.loan_duration:list').value = ['2']

        form.getControl(name='form.widgets.IShortName.id').value = _id
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1
        form.submit(form.getControl(name='form.buttons.save').value)
        self.assertEqual(self.book.absolute_url() + '/' + _id + '/view', self.browser.url,
                         'Current URL should be default view for newly created loan')
        loan = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_BOOK_LOAN, id=_id)
        loan = loan[0]

        self.assertEqual(loan.getObject().student.to_object, self.student)
        self.assertEqual(loan.getObject().book.to_object, self.book)

        # Make sure events fired
        self.assertFalse(loan.getObject().is_lock)
        self.assertEqual(self.book.number_of_loan_copy, 1)

        book = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_BOOK, id=self.book.getId())[0]

        # Book stock should be decreased
        self.assertEqual(book.book_stock, 1)
        self.assertEqual(book.getObject().number_of_copy, 2)

    def test_book_stock_validator(self):
        """
        :return:
        """
        self.book.number_of_loan_copy += 2
        self.book.reindexObject()
        transaction.commit()

        _id = self.book.generateUniqueId(CONTENT_TYPE_BOOK_LOAN).replace('.', '-')

        _url = self.book.absolute_url() + '/++add++' + CONTENT_TYPE_BOOK_LOAN
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

        form.getControl(name='form.widgets.book').value = self.book.UID()
        form.getControl(name='form.widgets.student').value = self.student.UID()
        form.getControl(name='form.widgets.loan_duration:list').value = ['2']

        form.getControl(name='form.widgets.IShortName.id').value = _id
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1
        form.submit(form.getControl(name='form.buttons.save').value)
        self.assertNotEqual(
            self.book.absolute_url() + '/' + _id + '/view',
            self.browser.url,
            'Current URL should not be default view, because of validation error.')

        html_output = BeautifulSoup(self.browser.contents.strip('\n'), 'lxml')
        portal_message = html_output.find('dl', class_='portalMessage')

        error = portal_message.find('dt')

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

        super(TestBookLoanBrowser, self).tearDown()


def test_suite():
    """
    :return:
    """
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestBookLoan, prefix='test'))
    suite.addTest(unittest.makeSuite(TestBookLoanBrowser, prefix='test'))

    return suite
