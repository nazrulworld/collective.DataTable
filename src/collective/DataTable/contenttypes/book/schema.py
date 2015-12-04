# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model
from plone.autoform import directives as form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage

from collective.DataTable import _

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class BookSchema(model.Schema):

    """

    """

    title = schema.TextLine(
        title=_("Book Title"),
        required=True
    )

    description = schema.Text(
        title=_("Book Description"),
        required=False
    )

    isbn = schema.TextLine(
        title=_("ISBN"),
        required=True
    )

    details = RichText(
        title=_("Detail of the book"),
        required=False,
    )

    publisher = schema.TextLine(
        title=_("Publisher"),
        required=False
    )

    author = schema.TextLine(
        title=_("Author"),
        required=False
    )

    number_of_copy = schema.Int(
        title=_("Number of Copy"),
        required=True
    )

    number_of_loan_copy = schema.Int(
        title=_("Number of Loan"),
        required=False
    )
    form.omitted('number_of_loan_copy')

    cover_photo = NamedBlobImage(
         title=_("Cover Photo"),
         required=False
    )

__all__ = ("BookSchema", )
