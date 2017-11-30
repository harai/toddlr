import json
import logging
import os

import requests

from toddlr import datetime
from toddlr.exception import RetriableError, UnretriableError
from toddlr.todoist import mapping, util

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

env = os.environ


def params(**kwargs):
  p = {'token': env['TODOIST_API_KEY']}
  p.update(kwargs)
  return p


def request(method, url, params=None, data=None, headers=None):
  log.info('Method: {}'.format(method))
  log.info('URL: {}'.format(url))
  log.info('Params: {}'.format(json.dumps(params)))
  log.info('Data: {}'.format(json.dumps(data)))
  log.info('Headers: {}'.format(json.dumps(headers)))

  res = getattr(requests, method)(
      url,
      params=params,
      data=None if data is None else json.dumps(data),
      headers=headers)

  log.info('Response Status Code: {}'.format(res.status_code))
  # CaseInsensitiveDict -> dict
  log.info('Response Headers: {}'.format(json.dumps(dict(res.headers))))
  if res.headers.get('content-type') == 'application/json':
    bodystr = json.dumps(res.json())
  else:
    bodystr = res.text
  log.info('Response Body: {}'.format(bodystr))

  status = res.status_code // 100
  if status == 5:
    try:
      res.raise_for_status()
    except Exception as e:
      raise RetriableError() from e
  if status == 4:
    if res.text == 'Sync item already processed. Ignored':
      return res
    raise UnretriableError()

  return res


def show_word(user, word, forgetful, note, project_id, base_request_id, now):
  headers = {
      'Content-Type': 'application/json',
      'X-Request-Id': util.request_id(base_request_id, user, word),
  }

  request(
      'post',
      'https://beta.todoist.com/API/v8/tasks',
      params=params(),
      data={
          'content': mapping.word_to_todoist(word),
          'project_id': project_id,
          'priority': mapping.forgetful_to_todoist(forgetful),
          'due_date': datetime.as_date_str(
              datetime.next_day(datetime.to_jst(now))),
      },
      headers=headers)


def clear_archived_word(task_id):
  request(
      'post',
      'https://beta.todoist.com/API/v8/tasks/{}/close'.format(task_id),
      params=params())


def get_archived_words(project_id):

  def get_note(items):
    for i in items:
      if not util.is_valid_todo(i):
        return i['content'].strip()
    return ''

  def add_note(item, note):
    if note is not None:
      item['_note'] = note
      return item

  res = request(
      'get',
      'https://beta.todoist.com/API/v8/tasks',
      params=params(project_id=project_id))

  items = res.json()
  note = get_note(items)
  return [add_note(i, note) for i in items]
