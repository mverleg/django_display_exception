# -*- coding: utf-8 -*-

"""
	for installing with pip
"""

from distutils.core import setup
from setuptools import find_packages

setup(
	name='django-display-exception',
	version='v0.1',
	author='Mark V',
	author_email='mdilligaf@gmail.com',
	packages=['display_exception'],
	include_package_data=True,
	url='git+https://github.com/mverleg/django_display_exception',
	license='Revised BSD License',
	description='see README.rst',  #todo
	zip_safe=True,
	install_requires = [
	],
)
