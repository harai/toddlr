import json
import logging

import toddlr.dynamodb.request
import toddlr.todoist.request
from toddlr import datetime, exception
from toddlr.dynamodb import mapping
from toddlr.todoist import project

log = logging.getLogger(__name__)


@exception.handle_error
def lambda_handler(event, context):
  msg = decode_message(event)
  item = mapping.dynamo_to_item(msg)
  now = datetime.now()
  toddlr.todoist.request.show_word(
      user=item['user'],
      word=item['word'],
      forgetful=item['forgetful'],
      note=item['note'],
      project_id=project.inbox_project_id(item['reminder']),
      base_request_id=msg['_request_id'],
      now=now)
  toddlr.dynamodb.request.mark_as_showed(user=item['user'], word=item['word'])


def decode_message(event):
  return json.loads(event['Records'][0]['Sns']['Message'])
