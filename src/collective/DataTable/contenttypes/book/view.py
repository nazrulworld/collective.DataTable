# -*- coding: utf-8 -*-
# ++ This file `view.py` is generated at 11/30/15 5:33 PM ++
import os
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditView
from plone.dexterity.browser import view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from .form import AddForm, EditForm

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


class AddView(DefaultAddView):

    """
    """
    form = AddForm
    portal_type = 'collective.DataTable.Book'


class EditView(DefaultEditView):

    """
    """
    form = EditForm
    portal_type = 'collective.DataTable.Book'


class DefaultView(view.DefaultView):

    """
    """
    index = ViewPageTemplateFile('item.pt', os.path.dirname(os.path.abspath(view.__file__)))


__all__ = ('AddView', 'EditView', 'DefaultView', )
