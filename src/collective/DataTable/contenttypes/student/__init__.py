# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from plone.dexterity.content import Container

from .interface import IStudent

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

__all__ = ("Student", "IStudent", )
