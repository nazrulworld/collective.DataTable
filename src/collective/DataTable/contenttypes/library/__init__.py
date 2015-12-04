# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.dexterity.content import Container

from .interface import ILibrary

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class Library(Container):

    """
    """
    implements(ILibrary)

__all__ = ('Library', 'ILibrary', )

