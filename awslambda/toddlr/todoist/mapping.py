import logging
import os

from toddlr import datetime
from toddlr.todoist import util

log = logging.getLogger(__name__)

env = os.environ


def word_to_todoist(word):
  return util.to_dictionary_url(word.strip())


def forgetful_to_todoist(forgetful):
  return 3 if forgetful else 1


def note_to_todoist(note):
  return note.strip()


def todoist_to_word(s):
  return util.from_dictionary_url(s.strip())


def todoist_to_reminder(value, ampm):
  return datetime.replace_ampm(datetime.to_jst(datetime.parse(value)), ampm)


def todoist_to_forgetful(priority):
  if priority == 1:
    return False
  # Tolerate "priority in [2, 4]" since it's just a minor human error.
  return True


def todoist_to_user():
  return 'jharai'


def todoist_to_note(s):
  return s.strip()


def todoist_to_item(value, ampm):

  return {
      'user': todoist_to_user(),
      'word': todoist_to_word(value['content']),
      'reminder': todoist_to_reminder(value['due']['date'], ampm),
      'forgetful': todoist_to_forgetful(value['priority']),
      '_task_id': value['id'],
  }
