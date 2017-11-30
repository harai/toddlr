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


def show_log(show_function):
  return logs.LogGroup(
      'ShowLog',
      LogGroupName=lambda_log_name(show_function),
      RetentionInDays=30)


def showeach_log(showeach_function):
  return logs.LogGroup(
      'ShoweachLog',
      LogGroupName=lambda_log_name(showeach_function),
      RetentionInDays=30)


def archive_log(archive_function):
  return logs.LogGroup(
      'ArchiveLog',
      LogGroupName=lambda_log_name(archive_function),
      RetentionInDays=30)


def archiveeach_log(archiveeach_function):
  return logs.LogGroup(
      'ArchiveeachLog',
      LogGroupName=lambda_log_name(archiveeach_function),
      RetentionInDays=30)
