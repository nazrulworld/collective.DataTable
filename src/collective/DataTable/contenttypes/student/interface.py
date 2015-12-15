# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant

from .schema import StudentSchema
from .schema import _

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class DuplicateRollNumberValidationError(Invalid):

    __doc__ = _('The specified roll number is already exists!')


class IStudent(StudentSchema, Interface):
    """
    """
    pass

__all__ = ("IStudent", )
