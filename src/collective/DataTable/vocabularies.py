# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from . import _

__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'


class LoanDurationVocab(object):

    """
    """
    implements(IContextSourceBinder)

    def __init__(self, start=None, maximum=None):

        """
        :param start:
        :param maximum:
        :return:
        """
        self.start = start or 1
        self.maximum = maximum or 10

    def __call__(self, context):

        """
        :param context:
        :return:
        """
        terms = []

        for i in range(self.start, self.maximum + 1, 1):

            terms.append(SimpleVocabulary.createTerm(i, str(i), _(str(i) + ' day')))

        return SimpleVocabulary(terms)


def load_vocabulary(context, vocab):
    """
    :param context:
    :param vocab:
    :return:
    """
    factory = getUtility(IVocabularyFactory, vocab)

    vocabulary = factory(context)

    return vocabulary

__all__ = ("LoanDurationVocab", )

