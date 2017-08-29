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

import codecs
import os
import sys

from shutil import rmtree
from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'PySlowLoris'
DESCRIPTION = 'Small and simple tool for testing Slow Loris vulnerability'
URL = 'https://github.com/maxkrivich/slowloris/'
EMAIL = 'maxkrivich@gmail.com'
AUTHOR = 'Maxim Krivich'

ABOUT = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec (f.read(), ABOUT)


readme_file = os.path.join(here, 'README.md')
try:
    from m2r import parse_from_file
    LONG_DESCRIPTION = parse_from_file(readme_file)
except ImportError:
    with open(readme_file) as f:
        LONG_DESCRIPTION = f.read()


with codecs.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.sep.join(('.', 'dist')))
        except:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name=NAME,
    version=ABOUT['__version__'],
    packages=find_packages(exclude=('tests',)),
    url=URL,
    license='MIT',
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=REQUIREMENTS,
    include_package_data=True,
    zip_safe=True,
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
        'console_scripts': ['slowloris=PySlowLoris.cli:main'],
    },
    cmdclass={
        'publish': PublishCommand,
    },
)
