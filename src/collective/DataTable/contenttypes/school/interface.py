# -*- coding: utf-8 -*-
from zope.interface import Interface
from .schema import SchoolSchema
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class ISchool(Interface, SchoolSchema):
    """
    """

__all__ = ("ISchool", )