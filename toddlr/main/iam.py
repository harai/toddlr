import logging
from pprint import PrettyPrinter

from troposphere import GetAtt, Join, Ref, iam

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
                'Action': [
                    'dynamodb:BatchWriteItem',
                    'dynamodb:PutItem',
                ],
                'Resource': [GetAtt(words_table, 'Arn')],
            },
            {
                'Effect': 'Allow',
                'Action': 's3:GetObject',
                'Resource': ['*'],
            },
        ],
    }

  return iam.Role(
      'CsvimportLambdaRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(PolicyName='role', PolicyDocument=role_policy()),
      ])


def show_lambda_role(words_table, showeach_topic):

  def role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect':
                'Allow',
                'Action': [
                    'dynamodb:Query',
                ],
                'Resource': [
                    Join(
                        '', [
                            GetAtt(words_table, 'Arn'),
                            '/index/user_showed_reminder',
                        ]),
                ],
            },
            {
                'Effect': 'Allow',
                'Action': 'sns:Publish',
                'Resource': [Ref(showeach_topic)],
            },
        ],
    }

  return iam.Role(
      'ShowLambdaRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(PolicyName='role', PolicyDocument=role_policy()),
      ])


def showeach_lambda_role(words_table):

  def role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': [
                    'dynamodb:UpdateItem',
                ],
                'Resource': [GetAtt(words_table, 'Arn')],
            },
        ],
    }

  return iam.Role(
      'ShoweachLambdaRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(PolicyName='role', PolicyDocument=role_policy()),
      ])


def archive_lambda_role(archiveeach_topic):

  def role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': 'sns:Publish',
                'Resource': [Ref(archiveeach_topic)],
            },
        ],
    }

  return iam.Role(
      'ArchiveLambdaRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(PolicyName='role', PolicyDocument=role_policy()),
      ])


def archiveeach_lambda_role(words_table):

  def role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': [
                    'dynamodb:UpdateItem',
                ],
                'Resource': [GetAtt(words_table, 'Arn')],
            },
        ],
    }

  return iam.Role(
      'ArchiveeachLambdaRole',
      AssumeRolePolicyDocument=lambda_assume_role_policy(),
      Policies=[
          iam.Policy(PolicyName='lambda', PolicyDocument=lambda_role_policy()),
          iam.Policy(PolicyName='role', PolicyDocument=role_policy()),
      ])


def events_invoke_lambda_role():

  def assume_role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Principal': {
                    'Service': 'events.amazonaws.com',
                },
                'Action': 'sts:AssumeRole',
            },
        ],
    }

  def role_policy():
    return {
        'Version':
        '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Action': ['lambda:InvokeFunction'],
                'Resource': ['*'],
            },
        ],
    }

  return iam.Role(
      'EventsInvokeLambdaRole',
      AssumeRolePolicyDocument=assume_role_policy(),
      Policies=[iam.Policy(PolicyName='event', PolicyDocument=role_policy())])
