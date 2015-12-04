# -*- coding: utf-8 -*-
from z3c.form import validator
from zope.interface import implements
from plone.dexterity.content import Container

from collective.DataTable.validators import ISBNValidator
from .interface import IBook

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class Book(Container):

    """
    """
    implements(IBook)


# Set conditions for which fields the validator class applies
validator.WidgetValidatorDiscriminators(ISBNValidator, field=IBook['isbn'])

__all__ = ("Book", "IBook", )
