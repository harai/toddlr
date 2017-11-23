import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, Join, Ref, awslambda

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def csvimport_function(
    csvimport_lambda_role, words_table, s3_bucket, s3_key_value,
    csvimport_s3_versionid_value):
  return awslambda.Function(
      'CsvimportFunction',
      Code=awslambda.Code(
          S3Bucket=Ref(s3_bucket),
          S3Key=Join('', [s3_key_value, '/csvimport.zip']),
          S3ObjectVersion=csvimport_s3_versionid_value),
      Environment=awslambda.Environment(
          Variables={
              'WORDS_TABLE': Ref(words_table),
          }),
      Handler='csvimport.lambda_handler',
      Role=GetAtt(csvimport_lambda_role, 'Arn'),
      Runtime='python3.6',
      Timeout=60 * 5)
