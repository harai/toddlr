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
          AttributeName='forgetful', AttributeType='S'),
  ]


def words_gsis():
  return [
      dynamodb.GlobalSecondaryIndex(
          IndexName='reminder',
          KeySchema=[
              dynamodb.KeySchema(AttributeName='user', KeyType='HASH'),
              dynamodb.KeySchema(AttributeName='reminder', KeyType='RANGE'),
          ],
          Projection=dynamodb.Projection(ProjectionType='ALL'),
          ProvisionedThroughput=dynamodb.ProvisionedThroughput(
              ReadCapacityUnits=1, WriteCapacityUnits=1)),
      dynamodb.GlobalSecondaryIndex(
          IndexName='forgetful',
          KeySchema=[
              dynamodb.KeySchema(AttributeName='forgetful', KeyType='HASH'),
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
      KeySchema=[dynamodb.KeySchema(AttributeName='word', KeyType='HASH')],
      ProvisionedThroughput=dynamodb.ProvisionedThroughput(
          ReadCapacityUnits=1, WriteCapacityUnits=1))
