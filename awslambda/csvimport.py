import logging
import os
from csv import DictReader
from io import StringIO

import boto3
from dateutil import parser

from toddlr import datetime, exception
from toddlr.dynamodb import request

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

env = os.environ

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')


@exception.handle_error
def lambda_handler(event, context):
  now = datetime.now()
  write_items(read_csv(event['s3_bucket'], event['s3_key'], now))


def read_csv(s3_bucket, s3_key, now):
  obj = s3.Object(s3_bucket, s3_key)
  for row in DictReader(StringIO(obj.get()['Body'].read().decode())):
    r = {}
    r['user'] = row.get('user', 'jharai').strip()
    r['word'] = row['word'].strip()
    r['reminder'] = parser.parse(row['reminder'].strip())
    r['forgetful'] = row.get('forgetful', '').strip() == 'True'
    r['note'] = row.get('note', '').strip()
    r['created_at'] = now
    yield r


def write_items(items):
  created_count = 0
  ignored_count = 0
  for i in items:
    created = request.create_word(
        user=i['user'],
        word=i['word'],
        reminder=i['reminder'],
        forgetful=i['forgetful'],
        note=i['note'],
        showed=False,
        created_at=i['created_at'])
    if created:
      created_count += 1
    else:
      ignored_count += 1
  log.info('Created {} words.'.format(created_count))
  log.info('Ignored {} words.'.format(ignored_count))
