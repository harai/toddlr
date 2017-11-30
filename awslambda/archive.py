import json
import logging
import os

import boto3

from toddlr import datetime, exception
from toddlr.todoist import project, request

log = logging.getLogger(__name__)

env = os.environ

sns = boto3.resource('sns')

archiveeach_topic = sns.Topic(env['ARCHIVEEACH_TOPIC'])


@exception.handle_error
def lambda_handler(event, context):
  now = datetime.now()
  ids = project.archive_project_ids(now)
  pass_words(ids['am'], 'am', context.aws_request_id)
  pass_words(ids['pm'], 'pm', context.aws_request_id)


def pass_words(project_id, ampm, aws_request_id):
  items = request.get_archived_words(project_id)
  publish(items, aws_request_id, ampm)


def publish(items, request_id, ampm):
  for i in items:
    i2 = i.copy()
    i2['_request_id'] = request_id
    i2['_ampm'] = ampm
    archiveeach_topic.publish(Message=json.dumps(i2, sort_keys=True))
