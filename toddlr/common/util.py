import logging
import os
import subprocess
from datetime import datetime
from pprint import PrettyPrinter

from troposphere import ImportValue, Join, Ref

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def current_git_revision():
  p = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
  return p.stdout.decode().strip()


def version_info():
  return 'Build URL: {}, Git revision: {}'.format(
      os.environ.get('CIRCLE_BUILD_URL', 'None'), current_git_revision())


def current_time():
  return datetime.now().strftime('%Y%m%d%H%M%S')


class Imp(object):

  def __init__(self, network_stack_name):
    self.network_stack_name = network_stack_name

  def ort(self, name):
    return ImportValue(Join('', [Ref(self.network_stack_name), ':', name]))


def get_code(path):
  with open(path, 'r') as f:
    return f.read()


def lambda_log_name(function):
  return Join('', [
      '/aws/lambda/',
      Ref(function),
  ])


def condition(template, name, cond):
  template.add_condition(name, cond)
  return name
