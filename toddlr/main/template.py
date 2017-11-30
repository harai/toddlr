import logging
from pprint import PrettyPrinter

from troposphere import Template

from toddlr.common import util
from toddlr.common.paramui import ParamUi
from toddlr.main import (
    awslambda,
    awslog,
    dynamodb,
    events,
    iam,
    output,
    param,
    predefined,
    sns
)

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def construct_csvimport(
    t, words_table, lambda_environment_dict, s3_bucket, s3_key_value):
  # Predefined
  csvimport_s3_versionid_value = util.versionid('csvimport')

  # IAM
  csvimport_lambda_role = t.add_resource(iam.csvimport_lambda_role(words_table))

  # Lambda
  csvimport_function = t.add_resource(
      awslambda.csvimport_function(
          csvimport_lambda_role=csvimport_lambda_role,
          lambda_environment_dict=lambda_environment_dict,
          s3_bucket=s3_bucket,
          s3_key_value=s3_key_value,
          csvimport_s3_versionid_value=csvimport_s3_versionid_value))

  # CloudWatch Logs
  t.add_resource(awslog.csvimport_log(csvimport_function))

  return csvimport_function


def construct_show(
    t, words_table, lambda_environment_dict, s3_bucket, s3_key_value,
    events_invoke_lambda_role):
  # Predefined
  showeach_s3_versionid_value = util.versionid('showeach')

  # IAM
  showeach_lambda_role = t.add_resource(iam.showeach_lambda_role(words_table))

  # Lambda
  showeach_function = t.add_resource(
      awslambda.showeach_function(
          showeach_lambda_role=showeach_lambda_role,
          lambda_environment_dict=lambda_environment_dict,
          s3_bucket=s3_bucket,
          s3_key_value=s3_key_value,
          showeach_s3_versionid_value=showeach_s3_versionid_value))

  # CloudWatch Logs
  t.add_resource(awslog.showeach_log(showeach_function))

  # SNS
  showeach_topic = t.add_resource(sns.showeach_topic(showeach_function))

  # Predefined
  show_s3_versionid_value = util.versionid('show')

  # IAM
  show_lambda_role = t.add_resource(
      iam.show_lambda_role(words_table, showeach_topic))

  # Lambda
  show_function = t.add_resource(
      awslambda.show_function(
          show_lambda_role=show_lambda_role,
          lambda_environment_dict=lambda_environment_dict,
          showeach_topic=showeach_topic,
          s3_bucket=s3_bucket,
          s3_key_value=s3_key_value,
          show_s3_versionid_value=show_s3_versionid_value))

  # CloudWatch Logs
  t.add_resource(awslog.show_log(show_function))

  # CloudWatch Events
  show_event_rule = t.add_resource(
      events.show_event_rule(events_invoke_lambda_role, show_function))

  # Lambda
  t.add_resource(
      awslambda.showeach_invocation_permission(
          showeach_function, showeach_topic))
  t.add_resource(
      awslambda.show_invocation_permission(show_function, show_event_rule))

  return show_function


def construct_archive(
    t, words_table, lambda_environment_dict, s3_bucket, s3_key_value,
    events_invoke_lambda_role):
  # Predefined
  archiveeach_s3_versionid_value = util.versionid('archiveeach')

  # IAM
  archiveeach_lambda_role = t.add_resource(
      iam.archiveeach_lambda_role(words_table))

  # Lambda
  archiveeach_function = t.add_resource(
      awslambda.archiveeach_function(
          archiveeach_lambda_role=archiveeach_lambda_role,
          lambda_environment_dict=lambda_environment_dict,
          s3_bucket=s3_bucket,
          s3_key_value=s3_key_value,
          archiveeach_s3_versionid_value=archiveeach_s3_versionid_value))

  # CloudWatch Logs
  t.add_resource(awslog.archiveeach_log(archiveeach_function))

  # SNS
  archiveeach_topic = t.add_resource(
      sns.archiveeach_topic(archiveeach_function))

  # Predefined
  archive_s3_versionid_value = util.versionid('archive')

  # IAM
  archive_lambda_role = t.add_resource(
      iam.archive_lambda_role(archiveeach_topic))

  # Lambda
  archive_function = t.add_resource(
      awslambda.archive_function(
          archive_lambda_role=archive_lambda_role,
          lambda_environment_dict=lambda_environment_dict,
          archiveeach_topic=archiveeach_topic,
          s3_bucket=s3_bucket,
          s3_key_value=s3_key_value,
          archive_s3_versionid_value=archive_s3_versionid_value))

  # CloudWatch Logs
  t.add_resource(awslog.archive_log(archive_function))

  # CloudWatch Events
  archive_event_rule = t.add_resource(
      events.archive_event_rule(events_invoke_lambda_role, archive_function))

  # Lambda
  t.add_resource(
      awslambda.archiveeach_invocation_permission(
          archiveeach_function, archiveeach_topic))
  t.add_resource(
      awslambda.archive_invocation_permission(
          archive_function, archive_event_rule))

  return archive_function


def construct_template():
  version = util.version_info()
  t = Template('Toddlr main - {}'.format(version))

  # Parameters
  pui = ParamUi()
  [
      todoist_api_key,
      archive_00_am,
      archive_00_pm,
      archive_10_am,
      archive_10_pm,
      archive_20_am,
      archive_20_pm,
      archive_30_am,
      archive_30_pm,
      archive_40_am,
      archive_40_pm,
      archive_50_am,
      archive_50_pm,
      inbox_0_sun_am,
      inbox_0_sun_pm,
      inbox_1_mon_am,
      inbox_1_mon_pm,
      inbox_2_tue_am,
      inbox_2_tue_pm,
      inbox_3_wed_am,
      inbox_3_wed_pm,
      inbox_4_thu_am,
      inbox_4_thu_pm,
      inbox_5_fri_am,
      inbox_5_fri_pm,
      inbox_6_sat_am,
      inbox_6_sat_pm,
  ] = param.todoist_group(pui, t)
  [
      google_project_id,
      google_private_key_id,
      google_private_key,
      google_client_email,
      spreadsheet_id,
  ] = param.spreadsheet_group(pui, t)
  [
      s3_bucket,
      s3_key_base,
  ] = param.s3_group(pui, t)

  pui.output(t)

  inbox = [
      {
          'am': inbox_0_sun_am,
          'pm': inbox_0_sun_pm,
      },
      {
          'am': inbox_1_mon_am,
          'pm': inbox_1_mon_pm,
      },
      {
          'am': inbox_2_tue_am,
          'pm': inbox_2_tue_pm,
      },
      {
          'am': inbox_3_wed_am,
          'pm': inbox_3_wed_pm,
      },
      {
          'am': inbox_4_thu_am,
          'pm': inbox_4_thu_pm,
      },
      {
          'am': inbox_5_fri_am,
          'pm': inbox_5_fri_pm,
      },
      {
          'am': inbox_6_sat_am,
          'pm': inbox_6_sat_pm,
      },
  ]

  archive = [
      {
          'am': archive_00_am,
          'pm': archive_00_pm,
      },
      {
          'am': archive_10_am,
          'pm': archive_10_pm,
      },
      {
          'am': archive_20_am,
          'pm': archive_20_pm,
      },
      {
          'am': archive_30_am,
          'pm': archive_30_pm,
      },
      {
          'am': archive_40_am,
          'pm': archive_40_pm,
      },
      {
          'am': archive_50_am,
          'pm': archive_50_pm,
      },
  ]

  # Predefined
  s3_key_value = predefined.s3_key_value(s3_key_base)

  # Role
  events_invoke_lambda_role = t.add_resource(iam.events_invoke_lambda_role())

  # DynamoDB
  words_table = t.add_resource(dynamodb.words_table())

  # Predefined
  lambda_environment_dict = predefined.lambda_environment_dict(
      words_table=words_table,
      todoist_api_key=todoist_api_key,
      inbox=inbox,
      archive=archive)

  # sub
  construct_csvimport(
      t,
      lambda_environment_dict=lambda_environment_dict,
      words_table=words_table,
      s3_bucket=s3_bucket,
      s3_key_value=s3_key_value)

  # sub
  construct_show(
      t,
      lambda_environment_dict=lambda_environment_dict,
      words_table=words_table,
      s3_bucket=s3_bucket,
      s3_key_value=s3_key_value,
      events_invoke_lambda_role=events_invoke_lambda_role)

  # sub
  construct_archive(
      t,
      lambda_environment_dict=lambda_environment_dict,
      words_table=words_table,
      s3_bucket=s3_bucket,
      s3_key_value=s3_key_value,
      events_invoke_lambda_role=events_invoke_lambda_role)

  # Output
  t.add_output([output.version(version)])

  return t


if __name__ == '__main__':
  print(construct_template().to_json(indent=2))
