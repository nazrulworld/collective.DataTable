# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model
from plone.autoform import directives as form
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree.source import ObjPathSourceBinder

from collective.DataTable import _
from collective.DataTable.vocabularies import LoanDurationVocab
from collective.DataTable.contenttypes.book import IBook
from collective.DataTable.contenttypes.student import IStudent

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class BookLoanSchema(model.Schema):

    """

    """
    book = RelationChoice(
        title=_("Select Book"),
        required=False,
        source=ObjPathSourceBinder(object_provides=IBook.__identifier__)
    )

    student = RelationChoice(
        title=_("Select Student"),
        required=False,
        source=ObjPathSourceBinder(object_provides=IStudent.__identifier__)
    )

    loan_duration = schema.Choice(
        title=_("Duration Days"),
        required=True,
        source=LoanDurationVocab()
    )

    loan_status = schema.Choice(
        title=_("Loan Status"),
        required=True,
        default='running',
        vocabulary=u"collective_DataTable_loan_status"
    )
    form.omitted('loan_status')

    is_locked = schema.Bool(
        title=_("This file is locked"),
        required=False
    )

__all__ = ("BookLoanSchema", )
