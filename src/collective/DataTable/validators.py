# -*- coding: utf-8 -*-
# ++ This file `validators.py` is generated at 11/22/15 5:36 PM ++
import re
from Acquisition import aq_inner
from plone.api.portal import get as getSite
from zope.interface import implementer, Invalid
from Products.CMFCore.utils import getToolByName
from z3c.form import interfaces
from z3c.form.validator import SimpleFieldValidator

from .vocabularies import load_vocabulary
from collective.DataTable import _
# from .contenttypes.book.interface import IBook
# from .contenttypes.school.interface import ISchool
# from .contenttypes.library.interface import ILibrary

from .constrains import CONTENT_TYPE_BOOK, CONTENT_TYPE_SCHOOL, CONTENT_TYPE_STUDENT, CONTENT_TYPE_LIBRARY

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"

# +++++++++++++ SimpleValidator +++++++++++++++++


class ISBNValidator(SimpleFieldValidator):

    """
    """
    def validate(self, value, force=False):
        """
        :param value:
        :param force
        :return:
        http://liswiki.org/wiki/International_Standard_Book_Number#Check_Digit_in_ISBN_13
        """
        super(ISBNValidator, self).validate(value, force)

        isbn_10_format = re.compile(r'^(ISBN )?[0-9]-?[0-9]{3}-?[0-9]{5}-?[0-9]$', re.IGNORECASE)
        isbn_13_format = re.compile(r'^(ISBN )?[0-9]{3}-?[0-9]-?[0-9]{3}-?[0-9]{5}-?[0-9]$', re.IGNORECASE)

        if isbn_13_format.match(value):

            self._validate_isbn_13_checksum(value)

        elif isbn_10_format.match(value):

            self._validate_isbn_10_checksum(value)

        else:
            raise Invalid(_('Invalid ISBN provided, valid format could be `ISBN 0-306-40615-2` or ` ISBN 978-0-306-40615-7`'))

        return True

    def _validate_isbn_13_checksum(self, value):

        """
        :param value
        :return:
        """
        # We will check valid number http://liswiki.org/wiki/International_Standard_Book_Number#Check_Digit_in_ISBN_13
        _value = value.split(' ')[-1].replace('-', '')
        _total = 0

        for index, num in enumerate(_value[:-1]):

            if index % 2 == 0:
                _total += int(num) * 1
            else:
                _total += int(num) * 3

        if int(_value[-1]) != (10 - (_total % 10)):
            raise Invalid(_('Invalid SSN: checksum error for 13 digit ssn.'))

    def _validate_isbn_10_checksum(self, value):

        """
        :param value:
        :return:
        """

        # We will check valid number http://liswiki.org/wiki/International_Standard_Book_Number#Check_Digit_in_ISBN_10
        _value = value.split(' ')[-1].replace('-', '')
        _total = 0
        for index, num in enumerate(_value[:-1]):

            _total += int(num) * (index + 1)

        if int(_value[-1]) != (_total % 11):

            raise Invalid(_('Invalid SSN: checksum error for 10 digit ssn.'))


class UniqueISBNValidator(SimpleFieldValidator):

    """
    """
    def validate(self, value, force=False):

        """
        :param value:
        :param force:
        :return:
        """
        super(UniqueISBNValidator, self).validate(value, force)

        library = aq_base(self.context)
        # assert ILibrary.providedBy(library), _('Context must be derived from content type `%s`' % CONTENT_TYPE_LIBRARY)

        portal_catalog = getToolByName(getSite(), 'portal_catalog')
        result = portal_catalog.searchResults(
            path='/'.join(library.getPhysicalPath()),
            portal_type=CONTENT_TYPE_BOOK,
            isbn=value,
            sort_limit=1)

        if result:
            raise Invalid(_("Provided ISBN Number `%s` is already exists!" % value))


class UniqueRollNumberValidator(SimpleFieldValidator):

    """
    """
    def validate(self, value, force=False):

        """
        :param value:
        :param force:
        :return:
        """
        super(UniqueRollNumberValidator, self).validate(value, force)
        # Custom validation here
        school = aq_inner(self.context)
        # assert ISchool.providedBy(school), _('Context must be derived from content type `%s`' % CONTENT_TYPE_SCHOOL)

        grade_widget = self.widget.form.widgets['grade']
        portal_catalog = getToolByName(getSite(), 'portal_catalog')

        result = portal_catalog.searchResults(
            path='/'.join(school.getPhysicalPath()),
            portal_type=CONTENT_TYPE_STUDENT,
            grade=grade_widget.value[0],
            roll_number=value,
            sort_limit=1
        )

        if result:

            raise Invalid(_("Provided Roll Number `%s` is already exists!" % value))


@implementer(interfaces.IValidator)
class BookStockValidator(object):

    """
    """
    def __init__(self, context, request=None):

        """
        :param context:
        :param request:
        :return:
        """
        self.context = context
        self.request = request

    def validate(self, value=None, force=False):

        """
        :param value:
        :param force:
        :return:
        """
        # assert IBook.providedBy(aq_base(self.context)), _('Context must be derived from content type `%s`'
        #                                                  % CONTENT_TYPE_BOOK)

        portal_catalog = getToolByName(getSite(), 'portal_catalog')
        book = portal_catalog.searchResults(path='/'.join(self.context.getPhysicalPath()), id=self.context.getId(),
                                            sort_limit=1)[0]

        if int(book.book_stock) < 1:

            raise Invalid(_("Insufficient stock of this book `%s`" % book.Title))

# +++++++++++++ constraints +++++++++++++++++


def constraint_grade(value):
    """
    :param value:
    :return:
    """
    grades = load_vocabulary(getSite(), 'collective_DataTable_grade')

    if value not in [grade.value for grade in grades]:

        raise Invalid(_('Grade value must be from `collective_DataTable_grade` vocabulary!'))

    return True


def isbn_validator(value):
    """
    :param value:
    :return:
    http://liswiki.org/wiki/International_Standard_Book_Number#Check_Digit_in_ISBN_13
    """
    isbn_10_format = re.compile(r'^(ISBN )?[0-9]-?[0-9]{3}-?[0-9]{5}-?[0-9]$', re.IGNORECASE)
    isbn_13_format = re.compile(r'^(ISBN )?[0-9]{3}-?[0-9]-?[0-9]{3}-?[0-9]{5}-?[0-9]$', re.IGNORECASE)

    if isbn_13_format.match(value):

        # We will check valid number http://liswiki.org/wiki/International_Standard_Book_Number#Check_Digit_in_ISBN_13
        _value = value.split(' ')[-1].replace('-', '')
        _total = 0
        for index, num in enumerate(_value[:-1]):

            if index % 2 == 0:
                _total += int(num) * 1
            else:
                _total += int(num) * 3

        if int(_value[-1]) != (_total % 10):

            raise Invalid(_('Invalid SSN: checksum error'))

    elif isbn_10_format.match(value):

        # We will check valid number http://liswiki.org/wiki/International_Standard_Book_Number#Check_Digit_in_ISBN_13
        _value = value.split(' ')[-1].replace('-', '')
        _total = 0
        for index, num in enumerate(_value[:-1]):

            _total += int(num) * (index + 1)

        if int(_value[-1]) != (_total % 11):

            raise Invalid(_('Invalid SSN: checksum error'))

    else:

        raise Invalid(_('Invalid ISBN provided, valid format could be `ISBN 0-306-40615-2` or ` ISBN 978-0-306-40615-7`'))

    return True

# +++++++++++++++++++++++++++++++++++++++++++

__all__ = (
    "constraint_grade",
    "BookStockValidator",
    "UniqueRollNumberValidator",
    "ISBNValidator",
    "UniqueISBNValidator")
