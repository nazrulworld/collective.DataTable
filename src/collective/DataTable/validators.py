# -*- coding: utf-8 -*-
# ++ This file `validators.py` is generated at 11/22/15 5:36 PM ++
import re
from Acquisition import aq_parent, aq_inner
from plone.api.portal import get as getSite
from zope.interface import Invalid
from z3c.form.validator import SimpleFieldValidator

from .vocabularies import load_vocabulary
#from .contenttypes.book_loan.interface import IBookLoan
from .testing import CONTENT_TYPE_BOOK_LOAN
from . import _

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"

# +++++++++++++ SimpleValidator +++++++++++++++++


class BookStockValidatorException(Invalid):
    pass


class BookStockValidator(SimpleFieldValidator):

    """
    """
    def validate(self, value, force=False):

        """
        :param value:
        :param force:
        :return:
        """
        super(BookStockValidator, self).validate(value, force)
        # Custom validation here
#        assert IBookLoan.providedBy(aq_inner(self.context)), _('Content Type must be %s' % CONTENT_TYPE_BOOK_LOAN)

        book = aq_parent(self.context)

        if int(book.number_of_copy) <= int(book.number_of_loan_copy):

            raise BookStockValidatorException(_("Insufficient stock of this book `%s`" % book.Title()))


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

        book = aq_parent(self.context)

        if int(book.number_of_copy) <= int(book.number_of_loan_copy):

            raise BookStockValidatorException(_("Insufficient stock of this book `%s`" % book.Title()))

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

__all__ = ("constraint_grade", "isbn_validator", "UniqueRollNumberValidator", "ISBNValidator", )
