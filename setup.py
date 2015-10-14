# -*- coding: utf-8 -*-

"""
	for installing with pip
"""

from distutils.core import setup


setup(
	name='django-display-exception',
	version='v0.4',
	author='Mark V',
	author_email='mdilligaf@gmail.com',
	packages=['display_exception'],
	include_package_data=True,
	url='https://github.com/mverleg/django_display_exception',
	license='Revised BSD License (LICENSE.txt)',
	description='This app can (sligtly) encourage modularity and readability, as well as decrease code repetition and length, by using Exceptions to handle exceptional (non-standard) situations.',
	zip_safe=True,
	install_requires = [
		'django',
	],
)
