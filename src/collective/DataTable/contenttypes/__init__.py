# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

# from .school import School
# from .student import Student
# from .library import Library
# from .book import Book
# from .book_review import BookReview


__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


def back_references(source_object, attribute_name):
    """
    :param source_object:
    :param attribute_name:
    :return: Return back references from source object on specified attribute_name
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                            dict(to_id=intids.getId(aq_inner(source_object)),
                                 from_attribute=attribute_name)
                            ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)

    return result

__all__ = ('back_references', )
