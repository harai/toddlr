import logging
from pprint import PrettyPrinter

from troposphere import Parameter, constants

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def todoist_group(pui, template):
  return pui.group(
      template, 'Todoist', [
          {
              'parameter': Parameter('TodoistApiKey', Type=constants.STRING),
              'label': 'Todoist API Key',
          },
          {
              'parameter': Parameter('Archive00Am', Type=constants.STRING),
              'label': 'Archive 00 AM',
          },
          {
              'parameter': Parameter('Archive00Pm', Type=constants.STRING),
              'label': 'Archive 00 PM',
          },
          {
              'parameter': Parameter('Archive10Am', Type=constants.STRING),
              'label': 'Archive 10 AM',
          },
          {
              'parameter': Parameter('Archive10Pm', Type=constants.STRING),
              'label': 'Archive 10 PM',
          },
          {
              'parameter': Parameter('Archive20Am', Type=constants.STRING),
              'label': 'Archive 20 AM',
          },
          {
              'parameter': Parameter('Archive20Pm', Type=constants.STRING),
              'label': 'Archive 20 PM',
          },
          {
              'parameter': Parameter('Archive30Am', Type=constants.STRING),
              'label': 'Archive 30 AM',
          },
          {
              'parameter': Parameter('Archive30Pm', Type=constants.STRING),
              'label': 'Archive 30 PM',
          },
          {
              'parameter': Parameter('Archive40Am', Type=constants.STRING),
              'label': 'Archive 40 AM',
          },
          {
              'parameter': Parameter('Archive40Pm', Type=constants.STRING),
              'label': 'Archive 40 PM',
          },
          {
              'parameter': Parameter('Archive50Am', Type=constants.STRING),
              'label': 'Archive 50 AM',
          },
          {
              'parameter': Parameter('Archive50Pm', Type=constants.STRING),
              'label': 'Archive 50 PM',
          },
          {
              'parameter': Parameter('Inbox0SunAm', Type=constants.STRING),
              'label': 'Inbox 0 Sun AM',
          },
          {
              'parameter': Parameter('Inbox0SunPm', Type=constants.STRING),
              'label': 'Inbox 0 Sun PM',
          },
          {
              'parameter': Parameter('Inbox1MonAm', Type=constants.STRING),
              'label': 'Inbox 1 Mon AM',
          },
          {
              'parameter': Parameter('Inbox1MonPm', Type=constants.STRING),
              'label': 'Inbox 1 Mon PM',
          },
          {
              'parameter': Parameter('Inbox2TueAm', Type=constants.STRING),
              'label': 'Inbox 2 Tue AM',
          },
          {
              'parameter': Parameter('Inbox2TuePm', Type=constants.STRING),
              'label': 'Inbox 2 Tue PM',
          },
          {
              'parameter': Parameter('Inbox3WedAm', Type=constants.STRING),
              'label': 'Inbox 3 Wed AM',
          },
          {
              'parameter': Parameter('Inbox3WedPm', Type=constants.STRING),
              'label': 'Inbox 3 Wed PM',
          },
          {
              'parameter': Parameter('Inbox4ThuAm', Type=constants.STRING),
              'label': 'Inbox 4 Thu AM',
          },
          {
              'parameter': Parameter('Inbox4ThuPm', Type=constants.STRING),
              'label': 'Inbox 4 Thu PM',
          },
          {
              'parameter': Parameter('Inbox5FriAm', Type=constants.STRING),
              'label': 'Inbox 5 Fri AM',
          },
          {
              'parameter': Parameter('Inbox5FriPm', Type=constants.STRING),
              'label': 'Inbox 5 Fri PM',
          },
          {
              'parameter': Parameter('Inbox6SatAm', Type=constants.STRING),
              'label': 'Inbox 6 Sat AM',
          },
          {
              'parameter': Parameter('Inbox6SatPm', Type=constants.STRING),
              'label': 'Inbox 6 Sat PM',
          },
      ])


def spreadsheet_group(pui, template):
  return pui.group(
      template, 'Spreadsheet', [
          {
              'parameter': Parameter('GoogleProjectId', Type=constants.STRING),
              'label': 'Google Project ID',
          },
          {
              'parameter': Parameter(
                  'GooglePrivateKeyId', Type=constants.STRING),
              'label': 'Google Private Key ID',
          },
          {
              'parameter': Parameter('GooglePrivateKey', Type=constants.STRING),
              'label': 'Google Private Key',
          },
          {
              'parameter': Parameter(
                  'GoogleClientEmail', Type=constants.STRING),
              'label': 'Google Client Email',
          },
          {
              'parameter': Parameter('SpreadsheetId', Type=constants.STRING),
              'label': 'Spreadsheet ID',
          },
      ])
