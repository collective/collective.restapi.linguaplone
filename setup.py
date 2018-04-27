# -*- coding: utf-8 -*-
"""Installer for the collective.restapi.linguaplone package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.restapi.linguaplone',
    version='2.0.0',
    description="An add-on providing plone.restapi endpoint for translations handled using LinguaPlone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='plone rest restful hypermedia api json',
    author='Mikel Larreategi',
    author_email='mlarreategi@codesyntax.com',
    url='https://pypi.python.org/pypi/collective.restapi.linguaplone',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.restapi'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.restapi',
        'Products.LinguaPlone',
        'setuptools',
        'Plone <= 4.99',
    ],
    extras_require={
        'test': [
            'collective.MockMailHost',
            'freezegun',
            'plone.app.testing [robot] >= 4.2.2',
            'plone.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'plone.api',
            'requests',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
