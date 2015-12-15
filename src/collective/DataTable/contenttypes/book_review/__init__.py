# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.dexterity.content import Item

from collective.DataTable.interfaces import IBookReview

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class BookReview(Item):

    """
    """
    implements(IBookReview)

__all__ = ("BookReview", )
