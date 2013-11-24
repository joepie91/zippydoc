#!/usr/bin/env python

"""
distutils/setuptools install script. See inline comments for packaging documentation.
"""

import os
import sys

try:
  from setuptools import setup
  # hush pyflakes
  setup
except ImportError:
  from distutils.core import setup

try:
  from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
  from distutils.command.build_py import build_py

packages = ['zippydoc']

package_dir = {"zippydoc": "src/zippydoc"}

package_data = {"zippydoc": ["data/template.html"]}

scripts = [
  'zpy2html'
]

print repr(package_data)

setup(
  name='zippydoc',
  version='1.1',
  maintainer='Sven Slootweg',
  maintainer_email='admin@cryto.net',
  description='Documentation markup language and library, including HTML converter.',
  url='http://www.cryto.net/zippydoc',
  packages=packages,
  package_dir=package_dir,
  package_data=package_data,
  include_package_data=True,
  scripts=scripts,
  install_requires=['argparse'],
  cmdclass={'build_py': build_py}
)

