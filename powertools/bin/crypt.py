#!/usr/bin/env python

from itertools import izip, starmap
from operator import xor
from struct import Struct
import argparse
import base64
import binascii
import getpass
import hashlib
import hashlib
import hmac
import logging
import os
import sys

from cryptography.fernet import Fernet


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


_pack_int = Struct('>I').pack


# Lifted from https://github.com/mitsuhiko/python-pbkdf2
def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None):
  """Like :func:`pbkdf2_bin` but returns a hex encoded string."""
  return pbkdf2_bin(data, salt, iterations, keylen, hashfunc).encode('hex')


# Lifted from https://github.com/mitsuhiko/python-pbkdf2
def pbkdf2_bin(data, salt, iterations=1000, keylen=24, hashfunc=None):
  """Returns a binary digest for the PBKDF2 hash algorithm of `data`
  with the given `salt`.  It iterates `iterations` time and produces a
  key of `keylen` bytes.  By default SHA-1 is used as hash function,
  a different hashlib `hashfunc` can be provided.
  """
  hashfunc = hashfunc or hashlib.sha1
  mac = hmac.new(data, None, hashfunc)
  def _pseudorandom(x, mac=mac):
    h = mac.copy()
    h.update(x)
    return map(ord, h.digest())
  buf = []
  for block in xrange(1, -(-keylen // mac.digest_size) + 1):
    rv = u = _pseudorandom(salt + _pack_int(block))
    for i in xrange(iterations - 1):
      u = _pseudorandom(''.join(map(chr, u)))
      rv = starmap(xor, izip(rv, u))
    buf.extend(rv)
  return ''.join(map(chr, buf))[:keylen]


def init_fernet(pass_prompt='Enter key'):
  password = getpass.getpass(pass_prompt)
  key = pbkdf2_hex(password, 'salt', iterations=1000, keylen=16, hashfunc=hashlib.sha512)
  safe = base64.b64encode(key)
  return Fernet(safe)


def encrypt(args):
  data = args.read()
  f = init_fernet(pass_prompt='Enter encrypt key:')
  enc = f.encrypt(data)
  sys.stdout.write(enc)


def decrypt(args):
  data = args.read()
  f = init_fernet(pass_prompt='Enter decrypt key:')
  dec = f.decrypt(data)
  sys.stdout.write(dec)


def enc():
  parser = argparse.ArgumentParser(description='Simple encrypt/decrypt tool.')
  args = parser.parse_args()
  encrypt(sys.stdin)


def dec():
  parser = argparse.ArgumentParser(description='Simple encrypt/decrypt tool.')
  args = parser.parse_args()
  decrypt(sys.stdin)
