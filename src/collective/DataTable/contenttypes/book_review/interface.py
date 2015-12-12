# -*- coding: utf-8 -*-
from zope.interface import Interface

from .schema import BookReviewSchema

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class IBookReview(BookReviewSchema, Interface):

    """
    """

__all__ = ("IBookReview", )
