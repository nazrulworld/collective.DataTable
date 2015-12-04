# -*- coding: utf-8 -*-
# ++ This file `events.py` is generated at 11/24/15 6:35 PM ++
import types
from Acquisition import aq_parent, aq_inner

__author__ = "Md Nazrul Islam<connect2nazrul@gmail.com>"


def collective_datatable_book_loan_created(obj, event):
    """
    :param obj:
    :param event:
    :return:
    """
    book_loan_obj = aq_inner(obj)
    book = aq_parent(book_loan_obj)

    if isinstance(book.number_of_loan_copy, types.NoneType):
        book.number_of_loan_copy = 0

    book.number_of_loan_copy += 1
    book_loan_obj.is_lock = False

    book.reindexObject(idxs=['Title', ])


def collective_datatable_book_loan_updated(obj, event):
    """
    :param obj:
    :param event:
    :return:
    """
    book_loan_obj = aq_inner(obj)
    if not book_loan_obj.is_lock and book_loan_obj.loan_status == 'returned':
        book = aq_parent(book_loan_obj)
        book.number_of_loan_copy -= 1
        book_loan_obj.is_lock = True

        book.reindexObject(idxs=['Title', ])


def collective_datatable_book_loan_removed(obj, event):
    """
    :param obj:
    :param event:
    :return:
    """
    book_loan_obj = aq_inner(obj)
    if not book_loan_obj.is_lock and book_loan_obj.loan_status != 'returned':
        book = aq_inner(book_loan_obj.oldParent)
        book.number_of_loan_copy -= 1

        book.reindexObject(idxs=['Title', ])

