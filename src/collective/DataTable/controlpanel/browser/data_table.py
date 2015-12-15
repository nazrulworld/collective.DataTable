# -*- coding: utf-8 -*-
# ++ This file `configuration.py` is generated at 12/13/15 8:28 PM ++
from plone.app.registry.browser import controlpanel
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button

from collective.DataTable import _
from collective.DataTable.interfaces import IConfiguration

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


class DataTableConfigurationForm(controlpanel.RegistryEditForm):

    id = "DataTable"
    label = _(u"heading_language_settings", default="DataTable Configuration")
    description = _(u"description_language_settings",
                    default="Settings related to DataTable and "
                            "report builder.")

    schema = IConfiguration
    schema_prefix = "collective.DataTable"

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        # # We need to check if the default language is in available languages
        # if 'default_language' in data and 'allowed_languages' in data and \
        #         data['default_language'] not in data['allowed_languages']:
        #     IStatusMessage(self.request).addStatusMessage(
        #         _(u"Default language not in available languages"),
        #         "error")
        #
        #     # e = Invalid(_(u"Default language not in available languages"))
        #     # raise WidgetActionExecutionError('default_language', e)
        #     return
        #
        # self.applyChanges(data)
        # IStatusMessage(self.request).addStatusMessage(
        #     _(u"Changes saved."),
        #     "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        pass
        # IStatusMessage(self.request).addStatusMessage(
        #     _(u"Changes canceled."),
        #     "info")
        # self.request.response.redirect("%s/%s" % (
        #     self.context.absolute_url(),
        #     self.control_panel_view))


class DataTableControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DataTableConfigurationForm
