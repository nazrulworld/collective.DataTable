# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
import zope.deferredimport

from collective.DataTable import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveDataTableLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


# Import Addons Configuration
zope.deferredimport.defineFrom(
    'collective.DataTable.controlpanel.interfaces',
    'IConfiguration'
)
# Import School Interface
zope.deferredimport.defineFrom(
    'collective.DataTable.contenttypes.school.interface',
    'ISchool',
)
# Import Library Interface
zope.deferredimport.defineFrom(
    'collective.DataTable.contenttypes.library.interface',
    'ILibrary'
)
# Import Student Interface
zope.deferredimport.defineFrom(
    'collective.DataTable.contenttypes.student.interface',
    'IStudent'
)
# Import Book Interface
zope.deferredimport.defineFrom(
    'collective.DataTable.contenttypes.book.interface',
    'IBook'
)
# Import Book Loan Interface
zope.deferredimport.defineFrom(
    'collective.DataTable.contenttypes.book_loan.interface',
    'IBookLoan'
)
# Import Book Review Interface
zope.deferredimport.defineFrom(
    'collective.DataTable.contenttypes.book_review.interface',
    'IBookReview'
)

