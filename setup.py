# -*- coding: utf-8 -*-
"""Installer for the collective.DataTable package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() +
    '\n' +
    'Contributors\n' +
    '============\n' +
    '\n' +
    open('CONTRIBUTORS.rst').read() +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')


setup(
    name='collective.DataTable',
    version='1.0a1',
    description="Data Table implementation into Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Md Nazrul Islam',
    author_email='email2nazrul@gmail.com',
    url='https://pypi.python.org/pypi/collective.DataTable',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'z3c.jbot',
        'plone.app.dexterity',
        'plone.rfc822',
        'plone.formwidget.contenttree',
        'plone.namedfile',
        'plone.formwidget.namedfile',
        'collective.vdexvocabulary',
        'collective.dexteritytextindexer',
        'plone.directives.form',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.mocktestcase',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)