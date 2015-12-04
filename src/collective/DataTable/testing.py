# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import z2

import collective.DataTable

CONTENT_TYPE_SCHOOL = 'collective.DataTable.School'
CONTENT_TYPE_STUDENT = 'collective.DataTable.Student'
CONTENT_TYPE_LIBRARY = 'collective.DataTable.Library'
CONTENT_TYPE_BOOK = 'collective.DataTable.Book'
CONTENT_TYPE_BOOK_LOAN = 'collective.DataTable.BookLoan'
CONTENT_TYPE_BOOK_REVIEW = 'collective.DataTable.BookReview'


class CollectiveDataTableMixin(object):
    pass


class CollectiveDataTableBrowserMixin(CollectiveDataTableMixin):
    """
    """
    def browser_login(self, user=None, password=None):

        user = user or TEST_USER_NAME
        password = password or TEST_USER_PASSWORD

        try:
            form = self.browser.getForm(id='login_form')

        except LookupError:

            self.browser.open(self.portal.absolute_url() + '/login')
            form = self.browser.getForm(id='login_form')

        form.getControl(name='__ac_name').value = user
        form.getControl(name='__ac_password').value = password

        form.submit(form.getControl(name='submit').value)

        if not self.browser.cookies.get('__ac'):

            raise ValueError(u"Login operation not success!, Please check manually.")



class CollectiveDataTableLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.DataTable)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.DataTable:default')


COLLECTIVE_DATATABLE_FIXTURE = CollectiveDataTableLayer()


COLLECTIVE_DATATABLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DATATABLE_FIXTURE,),
    name='CollectiveDataTableLayer:IntegrationTesting'
)


COLLECTIVE_DATATABLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DATATABLE_FIXTURE,),
    name='CollectiveDataTableLayer:FunctionalTesting'
)


COLLECTIVE_DATATABLE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_DATATABLE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveDataTableLayer:AcceptanceTesting'
)
