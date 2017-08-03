#! venv/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SlowLoris',
    version='1.2',
    packages=['slowloris'],
    url='https://github.com/maxkrivich/slowloris/',
    download_url='',
    license='MIT',
    author='Maxim Krivich',
    author_email='maxkrivich@gmail.com',
    description='Small and simple tool for testing Slow Loris vulnerability.',
    install_requires=requirements,
    keywords=['SlowLoris','ddos','slowloris','ddos','apache','ddos-attacks','denial-of-service','http','exploit','ddos-tool','hacker-scripts','hacking-tool','hacking','vulnerability','slow-requests','cybersecurity','cyber-security','information-security','security','server'],
)
