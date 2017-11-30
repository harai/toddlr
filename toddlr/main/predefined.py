import logging
from pprint import PrettyPrinter

from troposphere import Join, Ref

from toddlr.common import util

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def s3_key_value(s3_key_base):
  return Join(
      '', [
          Ref(s3_key_base),
          '/{}-{}'.format(
              util.current_git_revision(), 'dirty'
              if util.is_dirty() else 'clean'),
      ])


def lambda_environment_dict(words_table, todoist_api_key, inbox, archive):
  return {
      'INBOX':
      Join('|', [Join(',', [
          Ref(i['am']),
          Ref(i['pm']),
      ]) for i in inbox]),
      'ARCHIVE':
      Join('|', [Join(',', [
          Ref(a['am']),
          Ref(a['pm']),
      ]) for a in archive]),
      'WORDS_TABLE':
      Ref(words_table),
      'TODOIST_API_KEY':
      Ref(todoist_api_key),
  }
