import os
import json
from collections import OrderedDict
import re
from distutils.util import strtobool
import yaml
from bs4 import BeautifulSoup

from six.moves.urllib.request import urlopen


# pyyaml representer method for OrderedDict
def represent_odict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())


yaml.SafeDumper.add_representer(OrderedDict, represent_odict)


# For fields that should be double-quoted in resulting yaml should use this
# str wrapper class
class doublequoted_string(str):
    pass


# pyyaml representer method for doublequoted_string class defined above
def doublequoted_string_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='"')


yaml.SafeDumper.add_representer(
    doublequoted_string, doublequoted_string_representer)

method_dict = {}
base_url = 'https://api.slack.com/methods'

# api_spec_url = 'https://api.slack.com/specs/openapi/v2/slack_web.json'
# api_spec = json.loads(urlopen(api_spec_url).read())

api_doc_main = urlopen('%s/channels.invite' % base_url)

soup = BeautifulSoup(api_doc_main, 'html5lib')

api_methods = soup.find('select', id='api_method')

for method in api_methods.stripped_strings:
    if method == 'View another method...':
        continue

    method_dict[method] = {'params': OrderedDict()}
    method_url = '%s/%s' % (base_url, method)
    method_page = urlopen(method_url)
    method_soup = BeautifulSoup(method_page, 'html5lib')
    method_description = ('This action is auto-generated. See %s') % method_url
    method_dict[method]['description'] = method_description
    method_args_table = method_soup.find(
        'table', attrs={"class": "arguments full_width"}).tbody.find_all('tr')
    del method_args_table[0]
    for row in method_args_table:
        # assumes that first <code></code> contains the name of argument
        arg = row.find('code').text

        method_dict[method]['params'][arg] = {}

        required_col = row.find_all('td')[2]
        if re.search('Required', required_col.text):
            required = True
            default = None
        elif re.search(",", required_col.text):
            required, default_text = required_col.text.split(',')
            required = False
            default = default_text.split('=')[1]
        else:
            required = False
            default = None
        method_dict[method]['params'][arg]['required'] = required
        method_dict[method]['params'][arg]['default'] = default

        # description = row.find_all('td')[3].text.strip()
        # method_dict[method]['params'][arg]['description'] = description

    # parse Preferred HTTP method
    method_facts_table = method_soup.find('h2', attrs={"id": "facts"}).findNext('table')
    preferred_method = method_facts_table.find(
        'th', text='Preferred HTTP method:').findNext('td').text.strip()
    method_dict[method]['http_method'] = preferred_method

for method in method_dict:

    actions_dir = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../actions'))
    file_name = '%s/%s.yaml' % (actions_dir, method)
    output_dict = {
        'name': method,
        'runner_type': 'python-script',
        'enabled': True,
        'entry_point': 'run.py',
        'description': doublequoted_string(method_dict[method]['description']),
        'parameters': OrderedDict(),
    }
    output_dict['parameters']['end_point'] = {
        'type': 'string',
        'immutable': True,
        'default': method,
    }
    output_dict['parameters']['http_method'] = {
        'type': 'string',
        'default': method_dict[method]['http_method'],
        'required': True,
    }

    for param in method_dict[method]['params']:
        if param == 'token':
            method_dict[method]['params'][param]['required'] = False

        output_dict['parameters'][param] = OrderedDict()

        output_dict['parameters'][param]['required'] = \
            method_dict[method]['params'][param]['required']

        if method_dict[method]['params'][param]['default'] is not None:
            output_dict['parameters'][param]['default'] = \
                doublequoted_string(method_dict[method]['params'][param]['default'])

        # output_dict['parameters'][param]['description'] = \
        #     method_dict[method]['params'][param]['description']

        output_dict['parameters'][param]['type'] = 'string'

    # special care: text is not a mandatory parameter in chat.postMessage
    # https://github.com/slackhq/slack-api-docs/issues/41
    if method == 'chat.postMessage' or method == 'chat.update':
        output_dict['parameters']['text']['required'] = False

    # # update action description and parameter types from OpenAPI spec
    # http_method = output_dict['parameters']['http_method']['default'].lower()
    # path = '/%s' % method
    # method_api_spec = api_spec['paths'].get(path, {}).get(http_method)
    # if method_api_spec is not None:
    #     try:
    #         output_dict['description'] = method_api_spec['description']
    #     except KeyError:
    #         pass

    #     for param_name, param_value in output_dict['parameters'].items():
    #         param_spec = next(
    #             (p for p in method_api_spec['parameters'] if p['name'] == param_name), None)
    #         if param_spec is not None:
    #             try:
    #                 param_value['type'] = param_spec.get('type')
    #             except KeyError:
    #                 pass

    #             if param_value.get('default') is not None:
    #                 t = param_value['type']
    #                 if t == 'integer':
    #                     try:
    #                         param_value['default'] = int(param_value['default'])
    #                     except ValueError as e:
    #                         print '%s: %s: %s' % (method, param_name, e)
    #                         del param_value['default']
    #                 elif t == 'boolean':
    #                     try:
    #                         param_value['default'] = bool(strtobool(param_value['default']))
    #                     except ValueError as e:
    #                         print '%s: %s: %s' % (method, param_name, e)
    #                         del param_value['default']
    #                 elif t == 'number':
    #                     try:
    #                         param_value['default'] = float(param_value['default'])
    #                     except ValueError as e:
    #                         print '%s: %s: %s' % (method, param_name, e)
    #                         del param_value['default']

    print yaml.safe_dump(output_dict, default_flow_style=False, width=float('inf'))

    fh = open(file_name, 'w')
    fh.write(yaml.safe_dump(output_dict, default_flow_style=False, width=float('inf')))
    fh.close()
