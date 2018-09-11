#!/usr/bin/env python

from setuptools import setup, find_packages

NAME = "tkMagicGrid"
VERSION = "1.0.1"
AUTHOR = "Benjamin Johnson"
AUTHOR_EMAIL = "bmjcode@gmail.com"
DESCRIPTION = "Spreadsheet-like widget for Tkinter"

with open("README", "r") as readme:
    LONG_DESCRIPTION = readme.read()

URL = "https://github.com/bmjcode/tkMagicGrid"
PACKAGES = find_packages(exclude="test")
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url=URL,
      packages=PACKAGES,
      classifiers=CLASSIFIERS)
