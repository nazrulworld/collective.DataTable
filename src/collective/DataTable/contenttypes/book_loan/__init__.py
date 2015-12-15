# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.dexterity.content import Item

from collective.DataTable.interfaces import IBookLoan

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class BookLoan(Item):

    """
    """
    implements(IBookLoan)


__all__ = ("BookLoan", )
