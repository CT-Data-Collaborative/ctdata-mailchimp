#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from ctdata_mailchimp import __version__

REQUIREMENTS = [
    '',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='ctdata-mailchimp',
    version=__version__,
    description='Plugins for MailChimp integration.',
    author='Sasha Cuerda',
    author_email='scuerda@ctdata.org',
    url='https://github.com/CTData/ctdata-mailchimp',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
