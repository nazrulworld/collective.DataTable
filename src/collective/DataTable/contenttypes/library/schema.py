# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model

from collective.DataTable import _

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class LibrarySchema(model.Schema):

    """
    """
    title = schema.TextLine(
        title=_("Library Title")
    )
    description = schema.Text(
        title=_("Description of library")
    )

__all__ = ("LibrarySchema", )
