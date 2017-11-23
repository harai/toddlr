import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, iam

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def lambda_assume_role_policy():
  return {
      'Version':
      '2012-10-17',
      'Statement': [
          {
              'Effect': 'Allow',
              'Principal': {
                  'Service': 'lambda.amazonaws.com'
              },
              'Action': 'sts:AssumeRole'
          }
      ]
  }


def lambda_role_policy():
  return {
      'Version':
      '2012-10-17',
      'Statement': [
          {
              'Action': ['logs:*'],
              'Resource': 'arn:aws:logs:*:*:*',
              'Effect': 'Allow',
          },
          {
              # This action is not needed since LogGroup resource does that.
              'Action': ['logs:CreateLogGroup'],
              'Resource': 'arn:aws:logs:*:*:*',
              'Effect': 'Deny',
          },
          {
              'Action': ['lambda:*'],
              'Resource': '*',
              'Effect': 'Allow',
          },
          {
              'Effect': 'Allow',
              'Action': ['sns:Publish'],
              'Resource': ['*']
          },
      ],
  }


def csvimport_lambda_role(words_table):

  def role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': 'dynamodb:BatchWriteItem',
                'Resource': [GetAtt(words_table, 'Arn')],
            },
        ],
    }

  return iam.Role(
      'CsvimportLambdaRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(PolicyName='assume-role', PolicyDocument=role_policy()),
      ])
