# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.dexterity.content import Item

from .interface import IBookReview

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class BookReview(Item):

    """
    """

__all__ = ("BookReview", "IBookReview", )
