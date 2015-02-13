#!/usr/bin/env python

import os
import subprocess

from setuptools import setup, find_packages, Command


entry_points = {
  'console_scripts': [
    'vinit = powertools.bin.vinit:main',
    'bcp = powertools.bin.bcp:main',
    'enc = powertools.bin.crypt:enc',
    'dec = powertools.bin.crypt:dec',
  ],
}


class Pex(Command):

  user_options = []

  def initialize_options(self):
    """Abstract method that is required to be overwritten"""

  def finalize_options(self):
    """Abstract method that is required to be overwritten"""

  def run(self):
    if not os.path.exists('dist/wheel-cache'):
      print('You need to create dist/wheel-cache first! You\'ll need to run the following.')
      print('  mkdir dist/wheel-cache')
      print('  pip wheel -w dist/wheel-cache')
      return
    for entry in entry_points['console_scripts']:
      name, call = tuple([_.strip() for _ in entry.split('=')])
      print('Creating {0} as {1}'.format(name, call))
      subprocess.check_call([
        'pex',
        '-r', 'powertools',
        '--no-pypi',
        '--repo=dist/wheel-cache',
        '-o', name,
        '-e', call])


setup(
  name='powertools',
  version='0.0.4',
  description="Framework and utility code for running public key infrastructure.",
  author='Stephen Holsapple',
  author_email='sholsapp@gmail.com',
  url='https://github.com/sholsapp/powertools',
  packages=find_packages(),
  install_requires=[
    'cryptography',
  ],
  tests_require=[
    'pytest',
  ],
  entry_points=entry_points,
  cmdclass={'pexify': Pex},
)
