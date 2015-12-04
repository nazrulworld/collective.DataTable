# -*- coding: utf-8 -*-
# ++ This file `test_book.py` is generated at 11/22/15 7:22 AM ++
# Run Test: `bin/test -s collective.DataTable -m contenttypes -t test_book`
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

from collective.DataTable.contenttypes.book import IBook
from collective.DataTable.contenttypes.book.interface import book_stock
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

    self.school.invokeFactory(CONTENT_TYPE_LIBRARY, 'library')
    self.library = self.school['library']
    self.library.setTitle('My Test Library')

    self.school.reindexObject()

    if commit:
        transaction.commit()


class TestBook(unittest.TestCase):

    """
    """
    layer = COLLECTIVE_DATATABLE_INTEGRATION_TESTING

    def setUp(self):
        """
        :return:
        """
        self.school = None
        self.library = None

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.installer = api.portal.get_tool('portal_quickinstaller')

        init_fixture(self)

    def test_schema(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_BOOK)
        schema = fti.lookupSchema()

        self.assertEquals(schema, IBook)

    def test_factory(self):
        """
        :return:
        """
        fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE_BOOK)

        obj = createObject(fti.factory)

        self.assertTrue(IBook.providedBy(obj))

    def test_adding(self):
        """
        :return:
        """
        _id = safe_unicode('test-first-book')
        _title = safe_unicode('Test First Book')
        _isbn = safe_unicode('ISBN-01-90')

        self.library.invokeFactory(CONTENT_TYPE_BOOK, _id)
        book = self.library[_id]

        self.assertTrue(IBook.providedBy(book))

        book.setTitle(_title)
        book.isbn = _isbn

        book.reindexObject()

        result = self.portal.portal_catalog.searchResults(id=book.id)

        self.assertEquals(1, len(result))
        self.assertEqual(_title, result[0].Title)
        self.assertEquals(result[0].getObject().isbn, _isbn)

    def test_globally_add_not_allowed(self):
        """
        :return:
        """

        try:

            self.portal.invokeFactory(CONTENT_TYPE_BOOK, 'book')

        except ValueError, exc:

            self.assertIn('disallowed', exc.message.lower())
            self.assertIn(CONTENT_TYPE_BOOK, exc.message)

        else:

            raise AssertionError("This code should not reach here!, Globally not allowed this content type.")

    def test_allow_add_bookloan_and_bookreview_types(self):

        """
        :return:
        """
        self.library.invokeFactory(CONTENT_TYPE_BOOK, 'book')
        book = self.library['book']
        book.setTitle('My Test Book')

        book.reindexObject()

        # we make sure, other than book loan and book library type allowed, should raise ValueError exception
        try:
            book.invokeFactory(CONTENT_TYPE_LIBRARY, 'library')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIn('disallowed', _msg.lower())
        self.assertIn(CONTENT_TYPE_LIBRARY, _msg)

        # Make sure Book Loan type allowed
        try:
            book.invokeFactory(CONTENT_TYPE_BOOK_LOAN, 'book-loan')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIsNone(_msg)

        # Make sure Book Loan type allowed
        try:
            book.invokeFactory(CONTENT_TYPE_BOOK_REVIEW, 'book-review')
            _msg = None

        except ValueError as exc:

            _msg = exc.message

        self.assertIsNone(_msg)

    def test_isbn_validator(self):
        """
        :return:
        """
        import zope.component
        from zope.interface import Invalid
        from z3c.form import interfaces
        from collective.DataTable.validators import ISBNValidator

        isbn_validator = zope.component.queryMultiAdapter((None, None, None, IBook['isbn'], None), interfaces.IValidator)

        self.assertTrue(isinstance(isbn_validator, ISBNValidator))

        valid_isbn_13 = safe_unicode('ISBN 978-0-306-40615-7')
        valid_isbn_13_without_prefix = safe_unicode('978-0-306-40615-7')
        valid_isbn_13_numeric = safe_unicode('9780306406157')
        valid_isbn_13_numeric_withprefix = safe_unicode('isbn 9780306406157')

        try:
            isbn_validator.validate(valid_isbn_13)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_13)

        try:
            isbn_validator.validate(valid_isbn_13_without_prefix)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_13_without_prefix)

        try:
            isbn_validator.validate(valid_isbn_13_numeric)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_13_numeric)

        try:
            isbn_validator.validate(valid_isbn_13_numeric_withprefix)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_13_numeric_withprefix)

        valid_isbn_10 = safe_unicode('ISBN 0-306-40615-2')
        valid_isbn_10_without_prefix = safe_unicode('0-306-40615-2')
        valid_isbn_10_numeric = safe_unicode('0306406152')
        valid_isbn_10_numeric_withprefix = safe_unicode('isbn 0306406152')

        try:
            isbn_validator.validate(valid_isbn_10)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_10)

        try:
            isbn_validator.validate(valid_isbn_10_without_prefix)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_10_without_prefix)

        try:
            isbn_validator.validate(valid_isbn_10_numeric)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_10_numeric)

        try:
            isbn_validator.validate(valid_isbn_10_numeric_withprefix)
        except Invalid:
            raise AssertionError("`%s` should be valid, please check at collective.DataTable.validators.ISBNValidator" %
                                 valid_isbn_10_numeric_withprefix)

        invalid_format_isbn_13 = safe_unicode('ISBN 9-780-306-40615-7')
        invalid_checksum_isbn_13 = safe_unicode('978-0-306-40615-5')
        invalid_length_isbn_13_numeric = safe_unicode('97803064061578')

        try:
            isbn_validator.validate(invalid_format_isbn_13)
            raise AssertionError("`%s` should be invalid formated, please check at "
                                 "collective.DataTable.validators.ISBNValidator" % invalid_format_isbn_13)
        except Invalid:
            pass

        try:
            isbn_validator.validate(invalid_checksum_isbn_13)
            raise AssertionError("`%s` should be invalid check digit, please check at "
                                 "collective.DataTable.validators.ISBNValidator" % invalid_checksum_isbn_13)
        except Invalid:
            pass

        try:
            isbn_validator.validate(invalid_length_isbn_13_numeric)
            raise AssertionError("`%s` should be invalid isbn, please check at "
                                 "collective.DataTable.validators.ISBNValidator" % invalid_length_isbn_13_numeric)
        except Invalid:
            pass

        invalid_format_isbn_10 = safe_unicode('ISBN 030-6-40615-2')
        invalid_checksum_isbn_10 = safe_unicode('0-306-40615-1')
        invalid_length_isbn_10_numeric = safe_unicode('03064061523')

        try:
            isbn_validator.validate(invalid_format_isbn_10)
            raise AssertionError("`%s` should be invalid formated, please check at "
                                 "collective.DataTable.validators.ISBNValidator" % invalid_format_isbn_10)
        except Invalid:
            pass

        try:
            isbn_validator.validate(invalid_checksum_isbn_10)
            raise AssertionError("`%s` should be invalid check digit, please check at "
                                 "collective.DataTable.validators.ISBNValidator" % invalid_checksum_isbn_10)
        except Invalid:
            pass

        try:
            isbn_validator.validate(invalid_length_isbn_13_numeric)
            raise AssertionError("`%s` should be invalid isbn, please check at "
                                 "collective.DataTable.validators.ISBNValidator" % invalid_length_isbn_10_numeric)
        except Invalid:
            pass


class TestBookBrowser(unittest.TestCase, CollectiveDataTableBrowserMixin):

    """
    """
    layer = COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING

    def setUp(self):
        """
        :return:
        """
        self.school = None
        self.library = None

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
        _id = safe_unicode('test-first-book')
        _title = safe_unicode('Test First Book')
        _description = safe_unicode('The test description')
        _details = safe_unicode('<h1>Test Book Details</h1>')
        _isbn = safe_unicode('ISBN 978-0-306-40615-7')
        _author = safe_unicode('Test Author')
        _publisher = safe_unicode('Test Publisher')
        _number_of_copy = safe_unicode('10')
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

        self.assertEqual(self.library.absolute_url() + '/' + _id + '/view', self.browser.url,
                         'Current URL should be default view for newly created book')
        book = self.portal.portal_catalog.searchResults(portal_type=CONTENT_TYPE_BOOK, id=_id)
        book = book[0]

        self.assertEqual(book.Title, _title)
        self.assertEqual(book.getObject().isbn, _isbn)

        # Test Indexer
        self.assertEqual(book_stock(book.getObject())(), book.book_stock)

        self.assertEqual(int(book.getObject().number_of_copy), int(_number_of_copy))

    def tearDown(self):
        """
        :return:
        """

        error_log = getToolByName(self.portal, 'error_log')

        if len(error_log.getLogEntries()):
            print error_log.getLogEntries()[-1]['tb_text']

        super(TestBookBrowser, self).tearDown()


def test_suite():
    """
    :return:
    """
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestBook, prefix='test'))
    suite.addTest(unittest.makeSuite(TestBookBrowser, prefix='test'))

    return suite

