#!/usr/bin/env python

"""Back up a file before destroying it.

Have you ever accidently copied over a file you actually didn't mean to blow
away? Use *bcp* to back up files before they're irrecoverably destroyed.

Use *bcp* in the following way.

  $ cat trash.txt
  I'm trash!
  $ cat important.txt
  I'm important!
  $ bcp trash.txt important.txt
  $ cat important.txt
  I'm trash!
  $ cat important.txt.2015-02-14-12-10-33
  I'm important!

"""

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

  parser = argparse.ArgumentParser(description=__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
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
