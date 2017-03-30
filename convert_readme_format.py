#!/usr/bin/env python

import pypandoc

long_description = pypandoc.convert('README.md', 'rst')
long_description = long_description.replace("\r","") # Do not forget this line
with open('README.rst','w',encoding="utf-8") as f:
       f.write(long_description)

