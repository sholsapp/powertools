#!/usr/bin/env python

"""Create a virtualenv.

Create a virtualenv using the current working direction as a name, which is
typically the project that you're isolating for development.

Use *vinit* in the following way.

  $ git clone https://github.com/sholsapp/powertools
  $ cd powertools
  $ vinit
  $ source activate
  $ python setup.py develop

"""

import argparse
import logging
import os
import shutil
import subprocess
import sys


logging.basicConfig(level=logging.INFO)


log = logging.getLogger(__name__)


default_virtualenv = os.path.join(
  os.path.expanduser('~'),
  '.virtualenvs',
  os.path.basename(os.getcwd())
)


def main():

  parser = argparse.ArgumentParser(description=__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-d', '--dest-directory', default=default_virtualenv,
                      help='Where to create the virtualenv instead of %(default)s.')
  parser.add_argument('-r', '--recreate', action='store_true',
                      help='Recreate the virtualenv if it already exists.')
  args = parser.parse_args()

  if not os.path.exists(args.dest_directory) or args.recreate:
    if os.path.exists(args.dest_directory):
      shutil.rmtree(args.dest_directory)
    subprocess.check_call([
      'virtualenv',
      args.dest_directory,
    ])

  if not os.path.exists('activate'):
    subprocess.check_call([
      'ln', '-s', os.path.join(args.dest_directory, 'bin', 'activate'), 'activate',
    ])

  print u"Congratulations! \U0001F37A"
