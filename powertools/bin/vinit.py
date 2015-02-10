#!/usr/bin/env python

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

  parser = argparse.ArgumentParser(description='Create or activate a virtualenv.')
  parser.add_argument('-d', '--dest-directory', default=default_virtualenv)
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

