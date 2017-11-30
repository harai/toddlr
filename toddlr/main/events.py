import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, events

from toddlr.common import util

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)

util.patch_events()


def show_event_rule(events_invoke_lambda_role, show_function):
  return events.Rule(
      'ShowEventRule',
      Description='Show words',
      RoleArn=GetAtt(events_invoke_lambda_role, 'Arn'),
      ScheduleExpression='cron(0/5 * * * ? *)',
      State='ENABLED',
      Targets=[
          events.Target(Arn=GetAtt(show_function, 'Arn'), Id='ShowFunction'),
      ])


def archive_event_rule(events_invoke_lambda_role, archive_function):
  return events.Rule(
      'ArchiveEventRule',
      Description='Archive words',
      RoleArn=GetAtt(events_invoke_lambda_role, 'Arn'),
      ScheduleExpression='cron(0/5 * * * ? *)',
      State='ENABLED',
      Targets=[
          events.Target(
              Arn=GetAtt(archive_function, 'Arn'), Id='ArchiveFunction'),
      ])
