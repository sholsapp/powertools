#!/usr/bin/env python

"""Poll a file.

Supports polling of local files or remote files.

"""

import argparse
import os
import requests
import sys
import time


class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


wheel = '|/-\\|/-\\'


def check(path):
  if os.path.exists(path):
    with open(path) as fh:
      return fh.read().strip()
  elif path.startswith('http'):
    return requests.get(path).text


def main():

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('target')
  args = parser.parse_args()

  x = 0
  contents = None

  while True:
    if not contents or x % 100 == 0:
      contents = check(args.target)
    print '\r({bcolors.OKBLUE}{wheel}{bcolors.ENDC}) - {contents}'.format(
      wheel=wheel[x % len(wheel)],
      contents=contents,
      bcolors=bcolors),
    sys.stdout.flush()
    time.sleep(0.1)
    x += 1


if __name__ == '__main__':
  main()
