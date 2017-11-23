import requests


def lambda_handler(event, context):
  return requests.get('https://google.com').status_code
