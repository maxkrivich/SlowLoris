#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2017 Maxim Krivich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import io
import os

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


setup(
    name='PySlowLoris',
    version='0.1.4',
    packages=['SlowLoris'],
    url='https://github.com/maxkrivich/slowloris/',
    download_url='',
    license='MIT',
    author='Maxim Krivich',
    author_email='maxkrivich@gmail.com',
    description='Small and simple tool for testing Slow Loris vulnerability.',
    long_description=read('README.rst'),
    install_requires=requirements,
    keywords=['SlowLoris', 'ddos', 'slowloris', 'ddos', 'apache', 'ddos-attacks', 'denial-of-service', 'http',
              'exploit', 'ddos-tool', 'hacker-scripts', 'hacking-tool', 'hacking', 'vulnerability', 'slow-requests',
              'cybersecurity', 'cyber-security', 'information-security', 'security', 'server'],
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': ['slowloris=SlowLoris.cli:main'],
    }
)
