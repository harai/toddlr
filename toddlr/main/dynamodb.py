import logging
from pprint import PrettyPrinter

from troposphere import dynamodb

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def words_attrdefs():
  return [
      dynamodb.AttributeDefinition(AttributeName='word', AttributeType='S'),
      dynamodb.AttributeDefinition(AttributeName='reminder', AttributeType='S'),
      dynamodb.AttributeDefinition(AttributeName='user', AttributeType='S'),
      dynamodb.AttributeDefinition(
          AttributeName='user/forgetful', AttributeType='S'),
      dynamodb.AttributeDefinition(
          AttributeName='user/showed', AttributeType='S'),
  ]


def words_gsis():
  return [
      dynamodb.GlobalSecondaryIndex(
          IndexName='user_showed_reminder',
          KeySchema=[
              dynamodb.KeySchema(AttributeName='user/showed', KeyType='HASH'),
              dynamodb.KeySchema(AttributeName='reminder', KeyType='RANGE'),
          ],
          Projection=dynamodb.Projection(ProjectionType='ALL'),
          ProvisionedThroughput=dynamodb.ProvisionedThroughput(
              ReadCapacityUnits=1, WriteCapacityUnits=1)),
      dynamodb.GlobalSecondaryIndex(
          IndexName='user_forgetful_reminder',
          KeySchema=[
              dynamodb.KeySchema(
                  AttributeName='user/forgetful', KeyType='HASH'),
              dynamodb.KeySchema(AttributeName='reminder', KeyType='RANGE'),
          ],
          Projection=dynamodb.Projection(ProjectionType='ALL'),
          ProvisionedThroughput=dynamodb.ProvisionedThroughput(
              ReadCapacityUnits=1, WriteCapacityUnits=1)),
  ]


def words_table():
  return dynamodb.Table(
      'WordsTable',
      AttributeDefinitions=words_attrdefs(),
      GlobalSecondaryIndexes=words_gsis(),
      KeySchema=[
          dynamodb.KeySchema(AttributeName='user', KeyType='HASH'),
          dynamodb.KeySchema(AttributeName='word', KeyType='RANGE'),
      ],
      ProvisionedThroughput=dynamodb.ProvisionedThroughput(
          ReadCapacityUnits=1, WriteCapacityUnits=1))
