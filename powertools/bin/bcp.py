#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import sys
import shutil


logging.basicConfig(level=logging.INFO)


log = logging.getLogger(__name__)


default_virtualenv = os.path.join(
  os.path.expanduser('~'),
  '.virtualenvs',
  os.path.basename(os.getcwd())
)


def main():

  parser = argparse.ArgumentParser(description='Back up a file before copying over it.')
  parser.add_argument('src')
  parser.add_argument('dst')
  args = parser.parse_args()

  src_path = os.path.abspath(args.src)
  dst_path = os.path.abspath(args.dst)

  if os.path.exists(dst_path):
    stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    shutil.copyfile(dst_path, '{0}.{1}'.format(dst_path, stamp))
  shutil.copyfile(src_path, dst_path)




if __name__ == '__main__':
  try:
    main()
    sys.exit(0)
  except Exception as e:
    log.exception('Unhandled exception.')
    sys.exit(1)
