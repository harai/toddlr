import logging
from pprint import PrettyPrinter

from troposphere import Template

from toddlr.common import util
from toddlr.common.paramui import ParamUi
from toddlr.main import dynamodb, output, param

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


def construct_template():
  version = util.version_info()
  t = Template('Toddlr main - {}'.format(version))

  # Parameters
  pui = ParamUi()
  [
      todoist_api_key,
      archive_00_am,
      archive_00_pm,
      archive_10_am,
      archive_10_pm,
      archive_20_am,
      archive_20_pm,
      archive_30_am,
      archive_30_pm,
      archive_40_am,
      archive_40_pm,
      archive_50_am,
      archive_50_pm,
      inbox_0_sun_am,
      inbox_0_sun_pm,
      inbox_1_mon_am,
      inbox_1_mon_pm,
      inbox_2_tue_am,
      inbox_2_tue_pm,
      inbox_3_wed_am,
      inbox_3_wed_pm,
      inbox_4_thu_am,
      inbox_4_thu_pm,
      inbox_5_fri_am,
      inbox_5_fri_pm,
      inbox_6_sat_am,
      inbox_6_sat_pm,
  ] = param.todoist_group(pui, t)
  [
      google_project_id,
      google_private_key_id,
      google_private_key,
      google_client_email,
      spreadsheet_id,
  ] = param.spreadsheet_group(pui, t)

  pui.output(t)

  # DynamoDB
  t.add_resource(dynamodb.words_table())

  # Output
  t.add_output([output.version(version)])

  return t


if __name__ == '__main__':
  print(construct_template().to_json(indent=2))
