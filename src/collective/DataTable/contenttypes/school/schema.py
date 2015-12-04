# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
# Develop Product Import Here
from collective.DataTable import _

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class SchoolSchema(model.Schema):

    title = schema.TextLine(
        title=_("School Title")
    )
    description = RichText(
        title=_("Description of school")
    )
    feature_photo = NamedBlobImage(
        title=_("Feature Image"),
        required=False
    )

__all__ = ("SchoolSchema", )
