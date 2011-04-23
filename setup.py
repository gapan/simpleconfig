# setup.py Install script for simpleconfig.py Copyright (C) 2011 George
# Vlahavas E-mail: vlahavas ~ at ~ gmail ~ dot ~ com

# This software is licensed under the terms of the GPLv3 license.

import sys
from distutils.core import setup 
from simpleconfig import __version__ as VERSION

NAME = 'simpleconfig'
MODULES = ['simpleconfig']
DESCRIPTION = 'Simple configuration file reading/writing'
URL = 'http://www.salixos.org'
LICENSE = 'GPLv3'
PLATFORMS = ["Platform Independent"]

setup(name = NAME,
      version = VERSION,
      description = DESCRIPTION,
      license = LICENSE,
      platforms = PLATFORMS,
      author = 'George Vlahavas',
      author_email = 'vlahavas ~ at ~ gmail ~ dot ~ com',
      url = URL,
      py_modules = MODULES,
     )
