# -*- coding: utf-8 -*-
from zope.interface import Interface

from .schema import BookLoanSchema

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class IBookLoan(Interface, BookLoanSchema):

    """
    """

__all__ = ("IBookLoan", )
