# -*- coding: utf-8 -*-
from zope.interface import Interface
from .schema import SchoolSchema
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class ISchool(SchoolSchema, Interface):
    """
    """

__all__ = ("ISchool", )
