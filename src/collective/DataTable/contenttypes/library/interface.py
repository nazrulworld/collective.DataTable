# -*- coding: utf-8 -*-
from zope.interface import Interface
from .schema import LibrarySchema

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class ILibrary(Interface, LibrarySchema):

    """
    """

__all__ = ("ILibrary", )