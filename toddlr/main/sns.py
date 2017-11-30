import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, sns

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def showeach_topic(showeach_function):
  return sns.Topic(
      'ShoweachTopic',
      Subscription=[
          sns.Subscription(
              Endpoint=GetAtt(showeach_function, 'Arn'), Protocol='lambda'),
      ])


def archiveeach_topic(archiveeach_function):
  return sns.Topic(
      'ArchiveeachTopic',
      Subscription=[
          sns.Subscription(
              Endpoint=GetAtt(archiveeach_function, 'Arn'), Protocol='lambda'),
      ])
