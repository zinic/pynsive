# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup, find_packages
    from setuptools.command import easy_install
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command import easy_install


def read(relative):
    contents = open(relative, 'r').read()
    return [l for l in contents.split('\n') if l != '']

setup(
    name='pynsive',
    version=read('VERSION')[0],
    description='A Python plugin and module introspection library.',
    long_description=open('README.rst', 'r').read(),
    author='John Hopper',
    author_email='john.hopper@jpserver.net',
    url='https://github.com/zinic/pynsive',
    download_url='https://pypi.python.org/pypi/pynsive',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Plugins',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3'
    ],
    tests_require=read('./tools/test-requires'),
    install_requires=read('./tools/install-requires'),
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']))
