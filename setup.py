#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: co0lc0der
:license: MIT
:copyright: (c) 2022-2023 co0lc0der
"""

version = '0.3.6'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='simple_query_builder',
    version=version,

    author='co0lc0der',
    author_email='c0der@ya.ru',

    description=(
        u'This is a small easy-to-use component for working with a database. '
        u'It provides some public methods to compose SQL queries and manipulate data. '
        u'Each SQL query is prepared and safe.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/co0lc0der/simple-query-builder-python',
    download_url='https://github.com/co0lc0der/simple-query-builder-python/archive/v{}.zip'.format(
        version
    ),

    license='MIT',

    packages=['simple_query_builder'],

    classifiers=[
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: SQL'
    ]
)
