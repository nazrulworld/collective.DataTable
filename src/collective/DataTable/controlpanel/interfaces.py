# -*- coding: utf-8 -*-
# ++ This file `interfaces.py` is generated at 12/13/15 6:57 PM ++
from zope import schema
from plone.supermodel import model
from zope.interface import Interface

from collective.DataTable import _

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


class IConfiguration(Interface):
    """
    """
    model.fieldset(
        'settings',
        label=_(u'Settings', default=u'Settings'),
        fields=[
            'is_server_side_process',
            'is_search_active',
            'is_filter_active',
            'is_sortable_active',
            'use_site_language_pref',
            'default_language',
            'allowed_languages']
    )

    is_server_side_process = schema.Bool(
        title=_(u"Active Server Process", default=u'Active Server Process'),
        required=False,
        default=False
    )

    is_search_active = schema.Bool(
        title=_(u'Active Full Text Search', default=u'Active Full Text Search'),
        required=False,
        default=False
    )

    is_filter_active = schema.Bool(
        title=_(u"Active Advanced Filter"),
        required=False,

    )

    is_sortable_active = schema.Bool(
        title=_(u"Active Sortable", default=u'Active Sortable')
    )

    use_site_language_pref = schema.Bool(
        title=_(u"User Site Language Preference", default=u"User Site Language Preference"),
        required=False,
        default=False
    )

    default_language = schema.Choice(
        title=_(u"heading_site_language",
                default=u"Site language"),
        description=_(
            u"description_site_language",
            default=u"The language used for the content and the UI "
                    u"of this site."),
        default='en',
        required=True,
        vocabulary="plone.app.vocabularies.AvailableContentLanguages"
    )

    allowed_languages = schema.List(
        title=_(u"heading_available_languages",
                default=u"Available languages"),
        description=_(u"description_available_languages",
                      default=u"The languages in which the site should be "
                              u"translatable."),
        required=True,
        default=['en'],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.AvailableContentLanguages"
        )
    )

    model.fieldset(
        'theming',
        label=_(u"Theming", default="Theming"),
        fields=['is_responsive', 'records_per_page', 'theme', 'custom_css']
    )

    is_responsive = schema.Bool(
        title=_(u'Responsive Layout?', default=u'Responsive Layout?'),
        required=False,
        default=True
    )

    records_per_page = schema.Choice(
        title=_(u"Records Per Page", default=u'Records Per Page'),
        default=u'50',
        required=True,
        vocabulary="collective_DataTable_records_per_page"
    )
    theme = schema.Choice(
        title=_(u"Choose Theme", default=u"Choose Theme"),
        required=True,
        vocabulary="collective_DataTable_themes",
        default="classic"
    )
    custom_css = schema.Text(
        title=_(u"Custom CSS", default=u'Custom CSS'),
        required=False,
    )

    model.fieldset(
        'plugins',
        label=_(u'Plugins', default=u"Plugins"),
        fields=['enable_search_highlight']
    )

    enable_search_highlight = schema.Bool(
        title=_(u'Enable Search Highlighter', default=u'Enable Search Highlighter'),
        required=False,
        default=False
    )

    model.fieldset(
        'query_building',
        label=_(u'Query Builder', default=u"Query Builder"),
        fields=['queries']
    )

    queries = schema.Dict(
        title=_(u'Query', default=u'Queries'),
        required=False,
        key_type=schema.TextLine(),
        value_type=schema.Text(required=False)
    )
