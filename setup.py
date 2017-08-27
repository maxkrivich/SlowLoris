#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SlowLoris',
    version='0.1.2',
    packages=['SlowLoris'],
    url='https://github.com/maxkrivich/slowloris/',
    download_url='',
    license='MIT',
    author='Maxim Krivich',
    author_email='maxkrivich@gmail.com',
    description='Small and simple tool for testing Slow Loris vulnerability.',
    install_requires=requirements,
    keywords=['SlowLoris', 'ddos', 'slowloris', 'ddos', 'apache', 'ddos-attacks', 'denial-of-service', 'http',
              'exploit', 'ddos-tool', 'hacker-scripts', 'hacking-tool', 'hacking', 'vulnerability', 'slow-requests',
              'cybersecurity', 'cyber-security', 'information-security', 'security', 'server'],
    classifiers=[
        'Development Status :: 0.1.2 - Beta',
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
        'console_scripts':['SlowLoris=cli:main'],
    }
)
