#!/usr/bin/env python

"""Create a virtualenv.

Create a virtualenv using the current working direction as a name. Why use the
current working directory to name the virtualenv? Typically, a project is
organized into a directory.

Take https://github.com/sholsapp/powertools. Use *vinit* in the following way.

  $ git clone https://github.com/sholsapp/powertools
  $ cd powertools
  $ vinit
  $ source activate
  $ python setup.py develop

"""

import argparse
import logging
import os
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

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('-d', '--dest-directory', default=default_virtualenv,
                      help="Where to create the virtualenv instead of %(default)s.")
  args = parser.parse_args()

  if not os.path.exists(args.dest_directory):
    subprocess.check_call([
      'virtualenv',
      args.dest_directory,
    ])

  subprocess.check_call([
    'ln', '-s', os.path.join(args.dest_directory, 'bin', 'activate'), 'activate',
  ])


if __name__ == '__main__':
  try:
    main()
    sys.exit(0)
  except Exception as e:
    log.exception('Unhandled exception.')
    sys.exit(1)

