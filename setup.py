#!/usr/bin/env python

"""
setup.py for vroom
"""

from distutils.core import setup, Extension

setup (
   name = 'vroom',
   version = '0.1.1',
   author = 'Jordan Van Aalsburg',
   author_email = 'jvan@cse.ucdavis.edu',
   url = 'http://iviz.csc.ucdavis.edu/vroom',
   description = 'Rapid development environment for virtual reality applications.',
   packages = ['vroom', 'vroom.core', 'vroom.rendering', 'vroom.utils', 'vroom.extra', 'vroom.extra.PLY'],
   scripts = ['bin/vroom'],
   requires = ['pyftgl', 'pyinotify', 'pyopengl', 'numpy']
   )
