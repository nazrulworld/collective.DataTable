# -*- coding: utf-8 -*-
from zope.interface import Interface

from .schema import BookReviewSchema

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class IBookReview(Interface, BookReviewSchema):

    """
    """

__all__ = ("IBookReview", )