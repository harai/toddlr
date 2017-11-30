import json
import logging

import toddlr.dynamodb.request
import toddlr.todoist.request
from toddlr import datetime, exception
from toddlr.todoist import mapping

log = logging.getLogger(__name__)


@exception.handle_error
def lambda_handler(event, context):
  now = datetime.now()
  msg = decode_message(event)
  item = mapping.todoist_to_item(msg, msg['_ampm'])

  toddlr.dynamodb.request.update_reminder(
      user=item['user'],
      word=item['word'],
      reminder=item['reminder'],
      forgetful=item['forgetful'],
      note=msg.get('_note', ''),
      showed=False,
      created_at=now)
  toddlr.todoist.request.clear_archived_word(item['_task_id'])


def decode_message(event):
  return json.loads(event['Records'][0]['Sns']['Message'])
