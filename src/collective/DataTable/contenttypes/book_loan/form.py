# -*- coding: utf-8 -*-
# ++ This file `form.py` is generated at 11/30/15 6:07 PM ++
from zope.interface import Invalid
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditForm
from Products.statusmessages.interfaces import IStatusMessage

from z3c.form import button
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError

from collective.DataTable import _
from collective.DataTable.validators import BookStockValidator
from collective.DataTable.constrains import CONTENT_TYPE_BOOK_LOAN

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


class AddForm(DefaultAddForm):
    """
    """
    portal_type = CONTENT_TYPE_BOOK_LOAN
    buttons = DefaultAddForm.buttons.omit('save',)

    success_message = _(u"Book Loan created")

    def __init__(self, context, request, ti=None):
        """
        :param context:
        :param request:
        :param ti:
        :return:
        """
        super(AddForm, self).__init__(context, request, ti)

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        """
        :param action:
        :return:
        """
        data, errors = self.extractData()

        stock_availability = BookStockValidator(self.context, self.request)
        try:
            stock_availability.validate()
        except Invalid, exc:
            raise ActionExecutionError(exc)

        if errors:
            self.status = self.formErrorsMessage
            return

        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(
                self.success_message, "info"
            )


class EditForm(DefaultEditForm):
    """
    """
    pass

__all__ = ('AddForm', 'EditForm', )
