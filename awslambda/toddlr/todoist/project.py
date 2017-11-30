import logging
import os

from toddlr import datetime

log = logging.getLogger(__name__)


def load_projects(s):

  def ampm(item):
    i = item.split(',')
    return {'am': int(i[0]), 'pm': int(i[1])}

  return [ampm(i) for i in s.split('|')]


inbox = load_projects(os.environ['INBOX'])
archive = load_projects(os.environ['ARCHIVE'])


def inbox_project_id(reminder):
  jstime = datetime.to_jst(reminder)
  return inbox[jstime.weekday()][datetime.ampm(jstime)]


def archive_project_ids(now):
  jstime = datetime.to_jst(now)
  return archive[jstime.minute // 10]
