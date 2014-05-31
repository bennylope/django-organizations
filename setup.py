#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import organizations

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    author="Ben Lopatin",
    author_email="ben@wellfire.co",
    name='django-organizations',
    version=organizations.__version__,
    description='Group accounts for Django',
    long_description=readme + '\n\n' + history,
    url='https://github.com/wellfire/django-organizations/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=[
        'organizations',
        'organizations.backends',
        'organizations.migrations',
        'organizations.templatetags',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
        'Django>=1.4.2,<1.8',
        'django-extensions>=0.9',
    ],
    include_package_data=True,
    zip_safe=False,
)
