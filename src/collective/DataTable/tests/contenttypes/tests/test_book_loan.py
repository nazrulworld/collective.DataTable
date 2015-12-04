# -*- coding: utf-8 -*-
# ++ This file `test_book.py` is generated at 11/30/15 6:38 PM ++
# Run Test: `bin/test -s collective.DataTable -m contenttypes -t test_book_review`
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import transaction
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
from collective.DataTable.testing import (
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

    self.library.invokeFactory(CONTENT_TYPE_BOOK, 'book')
    self.book = self.library['book']
    self.book.setTitle('My Test Book')

    self.book.details = safe_unicode('<h1>Test Book Details</h1>')
    self.book.isbn = safe_unicode('98-999-99-9999')
    self.book.author = safe_unicode('Test Author')
    self.book.publisher = safe_unicode('Test Publisher')
    self.book.number_of_copy = safe_unicode('10')

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


class TestBookReviewBrowser(unittest.TestCase, CollectiveDataTableBrowserMixin):

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

    def tearDown(self):
        """
        :return:
        """
        error_log = getToolByName(self.portal, 'error_log')

        if len(error_log.getLogEntries()):
            print error_log.getLogEntries()[-1]['tb_text']

        super(TestBookReviewBrowser, self).tearDown()

