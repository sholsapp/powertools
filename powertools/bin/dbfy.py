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
import sys

from sqlalchemy import create_engine, Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import click


Base = declarative_base()
session = sessionmaker()


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
    data = json.loads(sys.stdin.read())
  except Exception as e:
    click.secho('-', fg='red')
    sys.exit(1)

  fields = {
    '__tablename__': table,
    'id': Column(Integer, primary_key=True),
    'created': Column(DateTime, default=datetime.datetime.utcnow),
  }

  for data_key, data_value in data.iteritems():
    # TODO: Preserve the data value's type here, it's not hard, you're just
    # lazy and tired today...
    fields[data_key] = Column(String)

  def init(self, **kwargs):
    for kwarg in kwargs:
      setattr(self, kwarg, kwargs[kwarg])

  fields['__init__'] = init

  Table = type('Table', (Base,), fields)

  Base.metadata.create_all(engine)

  with session_scope() as s:
    t = Table(**data)
    s.add(t)

  click.secho('+', fg='green')
  sys.exit(0)
