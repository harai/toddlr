import datetime
import logging

from dateutil import parser

import pytz

log = logging.getLogger(__name__)

jst = pytz.timezone('Asia/Tokyo')


def now():
  return datetime.datetime.now().astimezone(tz=pytz.utc)


def to_jst(time):
  return time.astimezone(jst)


def ampm(dt):
  return dt.strftime('%p').lower()


def replace_ampm(dt, ampm):

  def hour():
    if ampm == 'am':
      return 4
    if ampm == 'pm':
      return 18
    raise ValueError('Illegal ampm: "{}"'.format(ampm))

  return datetime.datetime(
      dt.year, dt.month, dt.day, hour=hour(), tzinfo=dt.tzinfo)


def parse(s):
  return parser.parse(s)


def as_date_str(dt):
  return dt.strftime('%Y-%m-%d')


def next_day(dt):
  return dt + datetime.timedelta(1)
