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
        label=_('Settings', default=u'Settings'),
        fields=['use_site_language_pref', 'default_language', 'allowed_languages']
    )

    use_site_language_pref = schema.Bool(
        title=_("User Site Language Preference", default=u"User Site Language Preference"),
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
        label=_("Theming", u"Theming"),
        fields=['is_responsive', 'theme']
    )

    is_responsive = schema.Bool(
        title=_('Responsive Layout?', u'Responsive Layout?'),
        required=False,
        default=True
    )

    theme = schema.Choice(
        title=_("Choose Theme"),
        required=True,
        vocabulary="collective_DataTable_themes",
        default="classic"
    )

    model.fieldset(
        'plugins',
        label=_('Plugins', u"Plugins"),
        fields=['enable_search_highlight']
    )

    enable_search_highlight = schema.Bool(
        title=_('Enable Search Highlighter', u'Enable Search Highlighter'),
        required=False,
        default=False
    )

    model.fieldset(
        'query_building',
        label=_('Query Builder', default=u"Query Builder"),
        fields=['queries']
    )

    queries = schema.Dict(
        title=_('Query', default=u'Queries'),
        required=False,
        key_type=schema.TextLine(),
        value_type=schema.Text(required=False)
    )
