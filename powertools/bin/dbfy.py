"""Turn data into a row in a database.

Data is all around us in the form of JSON, CSV, TSV, HTML, and more, but it's
hard to keep track of over time. What's more, it's tedious to transform data in
all of its forms into structured data that you can watch over time.

This tool consumes data of various forms and turns it into a row in a SQLite
database. It tries to remove the tedious part of transforming data into a
structured database table by inferring the structure from the input data. This
tool is designed to be invoked periodically by an external scheduler like
crontab.

Try this a few times:

  .. highlight:: bash

    $ echo "{\"foo\":1,\"bar\":2}" | dbfy

Then admire your new data in your database named ./dbfy.db.

"""

from contextlib import contextmanager
import datetime
import json
import logging
import sys

from sqlalchemy import create_engine, Column, DateTime, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import click


log = logging.getLogger(__name__)


Base = declarative_base()
session = sessionmaker()


_type_map = {
  int: Integer,
  float: Float,
  basestring: String,
}


@contextmanager
def session_scope():
  """Provide a transactional scope around a series of operations."""
  s = session()
  try:
    yield s
    s.commit()
  except:
    s.rollback()
    raise
  finally:
    s.close()


@click.command()
@click.option('--database', default='dbfy.db',
              help='A sqlite database to use.')
@click.option('--table', default='Default',
              help='The table name to create or update.')
def main(database, table):

  engine = create_engine('sqlite:///{0}'.format(database))
  session.configure(bind=engine)

  try:
    raw = json.loads(sys.stdin.read())
  except Exception as e:
    click.secho('-', fg='red')
    sys.exit(1)

  if not isinstance(raw, list):
    raw = [raw]

  fields = {
    '__tablename__': table,
    'id': Column(Integer, primary_key=True),
    'created': Column(DateTime, default=datetime.datetime.utcnow),
  }

  for row_key, row_value in raw[0].iteritems():
    try:
      fields[row_key] = Column(_type_map[type(row_value)]())
    except Exception as e:
      log.debug('No mapping for type %s. Defaulting to storing as string.', type(row_value))
      click.secho('~', fg='yellow', nl=False)
      fields[row_key] = Column(String)

  def init(self, **kwargs):
    for kwarg in kwargs:
      setattr(self, kwarg, kwargs[kwarg])

  fields['__init__'] = init

  Table = type('Table', (Base,), fields)

  Base.metadata.create_all(engine)

  for row in raw:

    with session_scope() as s:
      t = Table(**row)
      s.add(t)
    click.secho('+', fg='green', nl=False)

  click.secho('')
  sys.exit(0)
