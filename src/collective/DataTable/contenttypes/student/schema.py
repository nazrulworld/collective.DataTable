# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model
from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage

from collective.DataTable import _
from collective.DataTable.validators import constraint_grade

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class StudentSchema(model.Schema):

    """   """
    title = schema.TextLine(
        title=u"Title",
        description=u"A title, which will be converted to a name",
        required=False,
    )
    form.omitted('title')

    first_name = schema.TextLine(
        title=_("First Name of Student"),
        required=True
    )

    last_name = schema.TextLine(
        title=_("Last Name of Student"),
        required=False
    )

    gender = schema.Choice(
        title=_("Gender"),
        required=True,
        vocabulary=u"collective_DataTable_gender"
    )
    roll_number = schema.Int(
        title=_("Roll Number"),
        required=True
    )

    grade = schema.Choice(
        title=_("Grade"),
        required=True,
        vocabulary=u"collective_DataTable_grade",
        constraint=constraint_grade
    )

    email = schema.TextLine(
        title=_("Email address"),
        required=False
    )

    contact_number = schema.TextLine(
        title=_("Contact Number")
    )

    address = schema.Text(
        title=_("Address"),
        required=False
    )
    profile_photo = NamedBlobImage(
        title=_("Student Photo"),
        required=False
    )

__all__ = ("StudentSchema", )
