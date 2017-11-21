import logging
from pprint import PrettyPrinter

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)


class ParamUi(object):

  def __init__(self):
    self._meta_groups = []
    self._meta_labels = {}

  def group(self, template, label, params):
    self._meta_groups.append(
        {
            'Label': {
                'default': label
            },
            'Parameters': [p['parameter'].name for p in params],
        })

    meta_labels = {p['parameter'].name: {'default': p['label']} for p in params}
    self._meta_labels.update(meta_labels)
    return [template.add_parameter(p['parameter']) for p in params]

  def output(self, template):
    template.add_metadata(
        {
            'AWS::CloudFormation::Interface': {
                'ParameterGroups': self._meta_groups,
                'ParameterLabels': self._meta_labels,
            },
        })
