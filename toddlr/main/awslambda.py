import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, Join, Ref, awslambda

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def csvimport_function(
    csvimport_lambda_role, lambda_environment_dict, s3_bucket, s3_key_value,
    csvimport_s3_versionid_value):
  return awslambda.Function(
      'CsvimportFunction',
      Code=awslambda.Code(
          S3Bucket=Ref(s3_bucket),
          S3Key=Join('', [s3_key_value, '/csvimport.zip']),
          S3ObjectVersion=csvimport_s3_versionid_value),
      Environment=awslambda.Environment(Variables=lambda_environment_dict),
      Handler='csvimport.lambda_handler',
      Role=GetAtt(csvimport_lambda_role, 'Arn'),
      Runtime='python3.6',
      Timeout=60 * 5)


def showeach_function(
    showeach_lambda_role, lambda_environment_dict, s3_bucket, s3_key_value,
    showeach_s3_versionid_value):
  return awslambda.Function(
      'ShoweachFunction',
      Code=awslambda.Code(
          S3Bucket=Ref(s3_bucket),
          S3Key=Join('', [s3_key_value, '/showeach.zip']),
          S3ObjectVersion=showeach_s3_versionid_value),
      Environment=awslambda.Environment(Variables=lambda_environment_dict),
      Handler='showeach.lambda_handler',
      Role=GetAtt(showeach_lambda_role, 'Arn'),
      Runtime='python3.6',
      Timeout=60 * 5)


def show_function(
    show_lambda_role, lambda_environment_dict, showeach_topic, s3_bucket,
    s3_key_value, show_s3_versionid_value):
  env = {
      'SHOWEACH_TOPIC': Ref(showeach_topic),
  }
  env.update(lambda_environment_dict)

  return awslambda.Function(
      'ShowFunction',
      Code=awslambda.Code(
          S3Bucket=Ref(s3_bucket),
          S3Key=Join('', [s3_key_value, '/show.zip']),
          S3ObjectVersion=show_s3_versionid_value),
      Environment=awslambda.Environment(Variables=env),
      Handler='show.lambda_handler',
      Role=GetAtt(show_lambda_role, 'Arn'),
      Runtime='python3.6',
      Timeout=60 * 5)


def archiveeach_function(
    archiveeach_lambda_role, lambda_environment_dict, s3_bucket, s3_key_value,
    archiveeach_s3_versionid_value):
  return awslambda.Function(
      'ArchiveeachFunction',
      Code=awslambda.Code(
          S3Bucket=Ref(s3_bucket),
          S3Key=Join('', [s3_key_value, '/archiveeach.zip']),
          S3ObjectVersion=archiveeach_s3_versionid_value),
      Environment=awslambda.Environment(Variables=lambda_environment_dict),
      Handler='archiveeach.lambda_handler',
      Role=GetAtt(archiveeach_lambda_role, 'Arn'),
      Runtime='python3.6',
      Timeout=60 * 5)


def archive_function(
    archive_lambda_role, lambda_environment_dict, archiveeach_topic, s3_bucket,
    s3_key_value, archive_s3_versionid_value):
  env = {
      'ARCHIVEEACH_TOPIC': Ref(archiveeach_topic),
  }
  env.update(lambda_environment_dict)

  return awslambda.Function(
      'ArchiveFunction',
      Code=awslambda.Code(
          S3Bucket=Ref(s3_bucket),
          S3Key=Join('', [s3_key_value, '/archive.zip']),
          S3ObjectVersion=archive_s3_versionid_value),
      Environment=awslambda.Environment(Variables=env),
      Handler='archive.lambda_handler',
      Role=GetAtt(archive_lambda_role, 'Arn'),
      Runtime='python3.6',
      Timeout=60 * 5)


def showeach_invocation_permission(showeach_function, showeach_topic):
  return awslambda.Permission(
      'ShoweachInvocationPermission',
      Action='lambda:InvokeFunction',
      FunctionName=Ref(showeach_function),
      Principal='sns.amazonaws.com',
      SourceArn=Ref(showeach_topic))


def archiveeach_invocation_permission(archiveeach_function, archiveeach_topic):
  return awslambda.Permission(
      'ArchiveeachInvocationPermission',
      Action='lambda:InvokeFunction',
      FunctionName=Ref(archiveeach_function),
      Principal='sns.amazonaws.com',
      SourceArn=Ref(archiveeach_topic))


def invocation_permission(name, function, event_rule):
  return awslambda.Permission(
      name,
      Action='lambda:InvokeFunction',
      FunctionName=Ref(function),
      Principal='events.amazonaws.com',
      SourceArn=GetAtt(event_rule, 'Arn'))


def show_invocation_permission(show_function, show_event_rule):
  return awslambda.Permission(
      'ShowInvocationPermission',
      Action='lambda:InvokeFunction',
      FunctionName=Ref(show_function),
      Principal='events.amazonaws.com',
      SourceArn=GetAtt(show_event_rule, 'Arn'))


def archive_invocation_permission(archive_function, archive_event_rule):
  return awslambda.Permission(
      'ArchiveInvocationPermission',
      Action='lambda:InvokeFunction',
      FunctionName=Ref(archive_function),
      Principal='events.amazonaws.com',
      SourceArn=GetAtt(archive_event_rule, 'Arn'))
