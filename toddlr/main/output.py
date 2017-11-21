import logging
from pprint import PrettyPrinter

from troposphere import Output

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def version(ver):
  return Output('Version', Value=ver)
