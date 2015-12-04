# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.dexterity.content import Container
from .interface import ISchool

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class School(Container):

    """
    """
    implements(ISchool)

__all__ = ("School", "ISchool", )
