# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from z3c.form import validator
from plone.dexterity.content import Container

from collective.DataTable.interfaces import IStudent
from collective.DataTable.validators import UniqueRollNumberValidator

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class Student(Container):
    """
    """
    implements(IStudent)

    def Title(self):
        """
        :return:
        """
        obj = aq_inner(self)

        return "{first_name} {last_name}".format(first_name=obj.first_name, last_name=obj.last_name)

# Make sure Unique Roll Number
validator.WidgetValidatorDiscriminators(UniqueRollNumberValidator, field=IStudent['roll_number'])

__all__ = ("Student", )

