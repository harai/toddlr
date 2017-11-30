import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key

from toddlr.dynamodb import mapping

log = logging.getLogger(__name__)

env = os.environ

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

words_table = dynamodb.Table(env['WORDS_TABLE'])


def get_words_to_show(user, now):
  hash = Key('user/showed').eq(mapping.user_showed_to_dynamo(user, False))
  range = Key('reminder').lt(mapping.date_to_dynamo(now))
  cond = hash & range

  next = True

  def q():
    nonlocal next
    start = {'ExclusiveStartKey': next} if isinstance(next, dict) else {}
    r = words_table.query(
        IndexName='user_showed_reminder',
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression=cond,
        **start)
    next = r.get('LastEvaluatedKey', False)
    yield from r['Items']

  while next:
    yield from q()


def create_word(user, word, reminder, forgetful, note, showed, created_at):
  try:
    # BatchWrite doesn't support ConditionalExpression.
    words_table.put_item(
        Item=mapping.item_to_dynamo(
            user, word, reminder, forgetful, note, showed, created_at),
        ConditionExpression=Attr('user').not_exists())
    return True
  except dynamodb_client.exceptions.ConditionalCheckFailedException:
    log.warning('Word already exists: "{}" ({})'.format(word, user))
    return False


def mark_as_showed(user, word):
  words_table.update_item(
      Key={
          'user': mapping.user_to_dynamo(user),
          'word': mapping.word_to_dynamo(word),
      },
      UpdateExpression='SET #n = :t',
      ConditionExpression=Attr('user').exists(),
      ExpressionAttributeNames={'#n': 'user/showed'},
      ExpressionAttributeValues={
          ':t': mapping.user_showed_to_dynamo(user, True)
      })


def update_reminder(user, word, reminder, forgetful, note, showed, created_at):
  words_table.update_item(
      Key={
          'user': mapping.user_to_dynamo(user),
          'word': mapping.word_to_dynamo(word),
      },
      UpdateExpression=(
          'SET '
          '#r = :r, '
          '#uf = :uf, '
          '#us = :us, '
          '#n = if_not_exists(#n, :n), '
          '#c = if_not_exists(#c, :c)'),
      ExpressionAttributeNames={
          '#r': 'reminder',
          '#uf': 'user/forgetful',
          '#us': 'user/showed',
          '#n': 'note',
          '#c': 'created_at',
      },
      ExpressionAttributeValues={
          ':r': mapping.reminder_to_dynamo(reminder),
          ':uf': mapping.user_forgetful_to_dynamo(user, forgetful),
          ':us': mapping.user_showed_to_dynamo(user, showed),
          ':n': mapping.note_to_dynamo(note),
          ':c': mapping.created_at_to_dynamo(created_at),
      })
