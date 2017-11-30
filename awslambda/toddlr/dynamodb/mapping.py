import logging

from dateutil import parser

import pytz

log = logging.getLogger(__name__)

dynamo_tz = pytz.timezone('Asia/Tokyo')


def bool_to_dynamo(b):
  return 'True' if b else 'False'


def date_to_dynamo(d):
  if d is None:
    return ''
  # Use custom format to be properly ordered and indexed.
  return d.astimezone(dynamo_tz).strftime('%Y-%m-%dT%H:%M:%S%z')


def dynamo_to_date(s):
  return None if s == '' else parser.parse(s)


def dynamo_to_bool(s):
  return s == 'True'


def item_to_dynamo(user, word, reminder, forgetful, note, showed, created_at):
  return {
      'user': user_to_dynamo(user),
      'word': word_to_dynamo(word),
      'reminder': reminder_to_dynamo(reminder),
      'user/forgetful': user_forgetful_to_dynamo(user, forgetful),
      'user/showed': user_showed_to_dynamo(user, showed),
      'note': note_to_dynamo(note),
      'created_at': created_at_to_dynamo(created_at),
  }


def dynamo_to_item(item):
  return {
      'user': dynamo_to_user(item['user']),
      'word': dynamo_to_word(item['word']),
      'reminder': dynamo_to_reminder(item['reminder']),
      'forgetful': dynamo_to_forgetful(item['user/forgetful']),
      'showed': dynamo_to_showed(item['user/showed']),
      'note': dynamo_to_note(item['note']),
      'created_at': dynamo_to_created_at(item['created_at']),
  }


def user_showed_to_dynamo(user, showed):
  return '{}/{}'.format(user_to_dynamo(user), bool_to_dynamo(showed))


def dynamo_to_showed(user_showed):
  return dynamo_to_bool(user_showed.split('/')[1])


def user_forgetful_to_dynamo(user, forgetful):
  return '{}/{}'.format(user_to_dynamo(user), bool_to_dynamo(forgetful))


def dynamo_to_forgetful(user_forgetful):
  return dynamo_to_bool(user_forgetful.split('/')[1])


def user_to_dynamo(user):
  return user.replace('/', ' ')


def dynamo_to_user(user):
  return user


def word_to_dynamo(word):
  return word.replace('/', ' ')


def dynamo_to_word(word):
  return word


def dynamo_to_reminder(reminder):
  return dynamo_to_date(reminder)


def reminder_to_dynamo(reminder):
  return date_to_dynamo(reminder)


def note_to_dynamo(note):
  # DynamoDB doesn't allow empty string
  return '${}'.format(note)


def dynamo_to_note(note):
  return note[1:]


def dynamo_to_created_at(created_at):
  return dynamo_to_date(created_at)


def created_at_to_dynamo(created_at):
  return date_to_dynamo(created_at)
