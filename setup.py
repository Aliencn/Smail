#!/usr/bin/env python
from setuptools import setup

with open('README.rst','r',encoding='utf-8') as f:
    readme = f.read()

setup(
    name='Smail',
    version='0.1.9',
    description='Python send mail',
    author='Alien',
    author_email='Aliencn@outlook.com',
    url='https://github.com/Aliencn/Smail',
    license='GPL',
    py_modules=['Smail'],
    long_description=readme,
)
