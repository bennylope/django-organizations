#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import organizations

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

py_version = sys.version_info

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")


dependencies = ["Django>=1.8.0", "typing>=3.6.4"]


setup(
    author="Ben Lopatin",
    author_email="ben@wellfire.co",
    name="django-organizations",
    version=organizations.__version__,
    description="Group accounts for Django",
    long_description=readme + "\n\n" + history,
    url="https://github.com/bennylope/django-organizations/",
    license="BSD License",
    platforms=["OS Independent"],
    packages=[
        "organizations",
        "organizations.backends",
        "organizations.migrations",
        "organizations.templatetags",
        "organizations.views",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Django",
    ],
    install_requires=dependencies,
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
)
