import logging
from pprint import PrettyPrinter

from troposphere import Join, Ref

from toddlr.common import util

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def s3_key_value(s3_key_base):
  return Join(
      '', [
          Ref(s3_key_base),
          '/{}-{}'.format(
              util.current_git_revision(), 'dirty'
              if util.is_dirty() else 'clean'),
      ])
