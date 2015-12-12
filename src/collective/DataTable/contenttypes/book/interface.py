# -*- coding: utf-8 -*-
from plone.indexer import indexer
from zope.interface import Interface

from .schema import BookSchema

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class IBook(BookSchema, Interface):

    """
    """


@indexer(IBook)
def book_stock(obj):

    number_of_loan_copy = obj.number_of_loan_copy

    if number_of_loan_copy is None:
        number_of_loan_copy = 0

    if obj.number_of_copy is None:

        return None

    return int(obj.number_of_copy) - int(number_of_loan_copy)

__all__ = ("IBook", )
