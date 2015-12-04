# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobFile
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.DataTable import _
from collective.DataTable.contenttypes.student import IStudent

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class BookReviewSchema(model.Schema):

    """
    """
    title = schema.TextLine(
        title=_("Title"),
        required=True,
    )

    description = RichText(
        title=_("Comment/Review"),
        required=True
    )

    attachment = NamedBlobFile(
        title=_("Attachment"),
        required=False
    )

    reviewer = RelationChoice(
        title=_("Reviewer"),
        required=False,
        source=ObjPathSourceBinder(object_provides=IStudent.__identifier__)
    )

__all__ = ("BookReviewSchema", )
