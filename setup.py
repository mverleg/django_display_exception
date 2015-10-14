# -*- coding: utf-8 -*-

"""
	for installing with pip
"""

from distutils.core import setup
import os


def gen_data_files(*dirs):
	results = []
	for src_dir in dirs:
		for root,dirs,files in os.walk(src_dir):
			results.append((root, map(lambda f:root + "/" + f, files)))
	return results
print(dict(gen_data_files('display_exception/templates/exceptions',)))

setup(
	name='django-display-exception',
	version='v0.6',
	author='Mark V',
	author_email='mdilligaf@gmail.com',
	packages=['display_exception'],
	#package_data={'display_exception': ['display_exception/templates/exceptions/base.html']},
	#package_data = dict(gen_data_files('display_exception/templates/exceptions',)),
	include_package_data=True,
	url='https://github.com/mverleg/django_display_exception',
	license='Revised BSD License (LICENSE.txt)',
	description='This app can (slightly) encourage modularity and readability, as well as decrease code repetition and length, by using Exceptions to handle exceptional (non-standard) situations.',
	zip_safe=True,
	install_requires = [
		'django',
	],
)
