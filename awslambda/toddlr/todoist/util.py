import logging
import os
import uuid
from urllib import parse
from uuid import UUID

log = logging.getLogger(__name__)

env = os.environ

uuid_namespace = UUID('{82b1fe08-fcba-401a-ac18-b54809c61789}')
weblio_prefix = 'https://ejje.weblio.jp/content/'


def request_id(base_request_id, user, word):
  s = '{}/{}/{}'.format(base_request_id, user, word)
  return str(uuid.uuid5(uuid_namespace, s))


def to_dictionary_url(word):
  return '{}{}'.format(weblio_prefix, parse.quote_plus(word))


def from_dictionary_url(content):
  url = content.split(' ', maxsplit=1)[0]
  if url.startswith(weblio_prefix):
    return parse.unquote_plus(url[len(weblio_prefix):])
  raise ValueError('Unknown URL format: "{}"'.format(url))


def is_valid_todo(todo):
  c = todo['content'].strip()
  if c.startswith(weblio_prefix):
    return True
  return False
