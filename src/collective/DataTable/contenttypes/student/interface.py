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


class IStudent(Interface, StudentSchema):
    """
    """

    @invariant
    def duplicate_roll_number_validate(self):

        """
        :return:
        """
        obj = aq_inner(self)
        return None
        portal_catalog = getToolByName(obj, 'portal_catalog')

        brains = portal_catalog.searchResults(
            object_provides=IStudent.__identifier__,
            path='/'.join(obj.aq_parent.getPhysicalPath()),
            grade=obj.grade,
            roll_number=obj.roll_number
        )

        if len(brains):

            raise DuplicateRollNumberValidationError(_('The specified roll number `%s` is already exists!' %
                                                       obj.roll_number))

__all__ = ("IStudent", )
