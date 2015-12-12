# -*- coding: utf-8 -*-
from zope.interface import Interface

from .schema import BookLoanSchema

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class IBookLoan(BookLoanSchema, Interface):

    """
    """

__all__ = ("IBookLoan", )
