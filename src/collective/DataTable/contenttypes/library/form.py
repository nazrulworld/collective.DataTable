# -*- coding: utf-8 -*-
# ++ This file `form.py` is generated at 11/30/15 4:47 PM ++
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditForm

from collective.DataTable import _
from collective.DataTable.constrains import CONTENT_TYPE_LIBRARY

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


class AddForm(DefaultAddForm):
    """
    """
    portal_type = CONTENT_TYPE_LIBRARY
    success_message = _(u"Library created")

    def __init__(self, context, request, ti=None):
        """
        :param context:
        :param request:
        :param ti:
        :return:
        """
        super(AddForm, self).__init__(context, request, ti)


class EditForm(DefaultEditForm):
    """
    """
    pass

__all__ = ('AddForm', 'EditForm', )
