import logging
from pprint import PrettyPrinter

from troposphere import Join, Ref, logs

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def lambda_log_name(function):
  return Join('', [
      '/aws/lambda/',
      Ref(function),
  ])


def csvimport_log(csvimport_function):
  return logs.LogGroup(
      'CsvimportLog',
      LogGroupName=lambda_log_name(csvimport_function),
      RetentionInDays=30)
