# -*- coding: utf-8 -*-
# ++ This file `data_table.py` is generated at 12/14/15 12:23 PM ++
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implementer
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.registry.interfaces import IRegistry

from collective.DataTable.interfaces import IConfiguration

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


@implementer(IConfiguration)
class DataTableControlPanelAdapter(object):
    """
    """
    adapts(IPloneSiteRoot)

    def __init__(self, plone_site_root):

        """
        :param plone_site_root:
        :return:
        """
        self.context = plone_site_root
        registry = getUtility(IRegistry)
        self.configurations = registry.forInterface(IConfiguration, prefix='collective.DataTable')

    def _get_is_server_side_process(self):
        """
        :return:
        """
        return self.configurations.is_server_side_process

    def _set_is_server_side_process(self, value):
        """
        :param value:
        :return:
        """
        self.configurations.is_server_side_process = value

    is_server_side_process = property(_get_is_server_side_process, _set_is_server_side_process)

    def _get_is_search_active(self):
        """
        :return:
        """
        return self.configurations.is_search_active

    def _set_is_search_active(self, value):
        """
        :param value:
        :return:
        """
        self.configurations.is_search_active = value

    is_search_active = property(_get_is_search_active, _set_is_search_active)

    def _get_is_filter_active(self):
        """
        :return:
        """
        return self.configurations.is_filter_active

    def _set_is_filter_active(self, value):
        """
        :param value:
        :return:
        """
        self.configurations.is_filter_active = value

    is_filter_active = property(_get_is_filter_active, _set_is_filter_active)

    def _get_is_sortable_active(self):
        """
        :return:
        """
        return self.configurations.is_sortable_active

    def _set_is_sortable_active(self, value):
        """
        :param value:
        :return:
        """
        self.configurations.is_sortable_active = value

    is_sortable_active = property(_get_is_sortable_active, _set_is_sortable_active)

    def _get_use_site_language_pref(self):
        """
        :return:
        """
        return self.configurations.use_site_language_pref

    def _set_use_site_language_pref(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.use_site_language_pref = value

    use_site_language_pref = property(_get_use_site_language_pref, _set_use_site_language_pref)

    def _get_default_language(self):
        """
        :return:
        """
        return self.configurations.default_language

    def _set_default_language(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.default_language = value

    default_language = property(_get_default_language, _set_default_language)

    def _get_allowed_languages(self):

        """
        :return:
        """
        return self.configurations.allowed_languages

    def _set_allowed_languages(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.allowed_languages = value

    allowed_languages = property(_get_allowed_languages, _set_allowed_languages)

    def _get_is_responsive(self):
        """
        :return:
        """
        return self.configurations.is_responsive

    def _set_is_responsive(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.is_responsive = value

    is_responsive = property(_get_is_responsive, _set_is_responsive)

    def _get_records_per_page(self):
        """
        :return:
        """
        return self.configurations.records_per_page

    def _set_records_per_page(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.records_per_page = value

    records_per_page = property(_get_records_per_page, _set_records_per_page)

    def _get_theme(self):
        """
        :return:
        """
        return self.configurations.theme

    def _set_theme(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.theme = value

    theme = property(_get_theme, _set_theme)

    def _get_custom_css(self):
        """
        :return:
        """
        return self.configurations.custom_css

    def _set_custom_css(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.custom_css = value

    custom_css = property(_get_custom_css, _set_custom_css)

    def _get_enable_search_highlight(self):
        """
        :return:
        """
        return self.configurations.enable_search_highlight

    def _set_enable_search_highlight(self, value):

        """
        :param value:
        :return:
        """
        self.configurations.enable_search_highlight = value

    enable_search_highlight = property(_get_enable_search_highlight, _set_enable_search_highlight)

    def _get_queries(self):

        """

        :return:
        """
        return self.configurations.queries

    def _set_queries(self, value):

        """
        :param value:
        :return:
        """

        self.configurations.queries = value

    queries = property(_get_queries, _set_queries)

