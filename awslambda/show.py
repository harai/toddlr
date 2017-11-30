import json
import logging
import os

import boto3

from toddlr import datetime, exception
from toddlr.dynamodb import request

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

env = os.environ

sns = boto3.resource('sns')

showeach_topic = sns.Topic(env['SHOWEACH_TOPIC'])


@exception.handle_error
def lambda_handler(event, context):
  now = datetime.now()
  publish(
      request.get_words_to_show(event.get('user', 'jharai'), now),
      context.aws_request_id)


def publish(items, request_id):
  count = 0
  for i in items:
    i2 = i.copy()
    i2['_request_id'] = request_id
    showeach_topic.publish(Message=json.dumps(i2, sort_keys=True))
    count += 1
  log.info('Started showing {} words.'.format(count))
