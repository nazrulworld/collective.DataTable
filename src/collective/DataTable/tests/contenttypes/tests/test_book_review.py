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

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles, login, logout
from plone.testing.z2 import Browser
from zope.component import (queryUtility, createObject)
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import safe_unicode

from collective.DataTable.contenttypes.book_review import IBookReview
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


class TestBookReview(unittest.TestCase):

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
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_BOOK_REVIEW)
        schema = fti.lookupSchema()

        self.assertEquals(schema, IBookReview)

    def test_factory(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_BOOK_REVIEW)

        obj = createObject(fti.factory)

        self.assertTrue(IBookReview.providedBy(obj))

    def test_adding(self):
        """
        :return:
        """
        _id = safe_unicode('test-first-review')
        _title = safe_unicode('Test First Review')

        self.book.invokeFactory(CONTENT_TYPE_BOOK_REVIEW, _id)
        review = self.book[_id]

        self.assertTrue(IBookReview.providedBy(review))

        review.setTitle(_title)
        review.reviewer = self.student.UID()

        review.reindexObject()

        result = self.portal.portal_catalog.searchResults(id=review.id)

        self.assertEquals(1, len(result))
        self.assertEqual(_title, result[0].Title)

    def test_globally_add_not_allowed(self):
        """
        :return:
        """

        try:

            self.portal.invokeFactory(CONTENT_TYPE_BOOK_REVIEW, 'book_review')

        except ValueError, exc:

            self.assertIn('disallowed', exc.message.lower())
            self.assertIn(CONTENT_TYPE_BOOK_REVIEW, exc.message)

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
        _resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        _id = safe_unicode('test-first-review')
        _title = safe_unicode('Test First Review')
        _description = safe_unicode('<h1>Test Book Review</h1>')
        _reviewer = self.student.UID()
        _attachment = 'test-review.pdf'

        _url = self.book.absolute_url() + '/++add++' + CONTENT_TYPE_BOOK_REVIEW
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
        form.getControl(name='form.widgets.reviewer').value = _reviewer

        form.getControl(name='form.widgets.IShortName.id').value = _id
        form.getControl(name='form.widgets.IExcludeFromNavigation.exclude_from_nav:list').value = 1
        form.getControl(name='form.widgets.INextPreviousToggle.nextPreviousEnabled:list').value = 1

        file_control = form.getControl(name='form.widgets.attachment')
        file_control.add_file(open(os.path.join(_resource_path, _attachment), 'rb'), 'application/pdf', _attachment)

        form.submit(form.getControl(name='form.buttons.save').value)

        self.assertEqual(self.book.absolute_url() + '/' + _id + '/view', self.browser.url,
                         'Current URL should be default view for newly created review')
        review = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_BOOK_REVIEW, id=_id)
        review = review[0]

        self.assertEqual(review.Title, _title)
        self.assertEqual(review.getObject().reviewer.to_object, self.student)
        self.assertEqual(review.getObject().attachment.filename, _attachment)

    def tearDown(self):
        """
        :return:
        """

        error_log = getToolByName(self.portal, 'error_log')

        if len(error_log.getLogEntries()):
            print error_log.getLogEntries()[-1]['tb_text']

        super(TestBookReviewBrowser, self).tearDown()

