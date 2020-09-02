#!/usr/bin/env python
# -*- coding: utf-8 -*-

# StdLib
import os
import json

# External
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import requests
import six
from prance import ResolvingParser

OPENAPI_JSON_URL = 'https://raw.githubusercontent.com/slackapi/slack-api-specs/master/web-api/slack_web_openapi_v2.json'  # noqa: E501

SLACK_SESSION = requests.Session()

METHOD_OVERRIDES = {
    'files.upload': {
        'entry_point': 'files_upload.py',
        'parameters': {
            # overriding content and file to modify their descriptions
            'content': {
                'name': 'content',
                'type': 'string',
                'required': False,
                'description': 'File contents via a POST variable. If omitting this parameter, you must provide either `file` or `file_path`.',  # noqa: E501
            },
            'file': {
                'name': 'file',
                'type': 'string',
                'required': False,
                'description': 'File contents via `multipart/form-data`. If omitting this parameter, you must provide either `file_path` or `content`.',  # noqa: E501
            },
            'file_path': {
                'name': 'file_path',
                'type': 'string',
                'required': False,
                'description': 'Path to the file on the local filesystem that will be opened, read and uploaded to Slack. If omitting this parameter, you must provide either `file` or `content`.',  # noqa: E501
            }
        }
    }
}

# Overriden by METHOD_OVERRIDES (more specific prefered over less specific)
GLOBAL_PARAM_OVERRIDES = {
    'token': {
        'required': False
    }
}


def get_openapi_spec():
    parser = ResolvingParser(OPENAPI_JSON_URL)
    return parser.specification  # contains fully resolved specs as a dict


def get_spec_from_http_reference(method):
    page = SLACK_SESSION.get("https://api.slack.com/methods/" + method)
    soup = BeautifulSoup(page.text, "lxml")

    # find the HTTP method
    method_facts_table = soup.find('h2', attrs={"id": "facts"}).findNext('table')
    method_header = method_facts_table.find('th', text='Preferred HTTP method:')
    http_method = method_header.findNext('td').text.strip()

    # find  <div class="method_arguments">
    # this is the table with all of the API parameters it in
    arguments_table = soup.find('div', class_='method_arguments full_width')
    # within this table, each argument has its own <div class="method_argument>
    arguments = arguments_table.find_all('div', class_='method_argument')
    params = {}
    for arg in arguments:
        # the name of this argument lives in a <span class="arg_name">
        arg_name = arg.find('span', class_='arg_name')
        # the actual name is a <a href=""> link and the argument is the text
        # within the link
        arg_name_link = arg_name.find('a')
        name = arg_name_link.text

        # the next thing we want to grab is the default value
        # this lives in its own <span class="arg_cell arg_desc">
        arg_desc = arg.find('span', class_="arg_cell arg_desc")
        # the default value lives in one of the paragraph <p> tags
        # so we find all of the <p> tags and try to search for the text "Default:"
        paragraphs = arg_desc.find_all('p')
        default = None
        for p in paragraphs:
            # we found a paragraph tag with our default value
            if 'Default:' in p.text:
                default = p.text.split('Default:')[1].strip()
                try:
                    # try to parse the default as JSON, this allows us to treat
                    # integers and booleans as their native type rather than as strings
                    # for everything
                    default = json.loads(default)
                except json.decoder.JSONDecodeError:
                    pass
            # save the default, we want to save this even if it's None so
            # that the template can skip defaults that are set to None
            params[name] = {'default': default}

    http_ref_spec = {
        'params': params,
        'http_method': http_method,
    }
    return http_ref_spec


def get_params_from_openapi_operation(openapi_operation, params_http_ref):
    parameters = {}
    for p in openapi_operation['parameters']:
        name = p['name']
        default = p.get('default')
        # if the OpenAPI spec doesn't have a default set (currently it does not)
        # try to grab the default from the HTTP reference documentation online
        if not default and name in params_http_ref:
            default = params_http_ref[name]['default']
        parameters[name] = {
            'name': name,
            'type': p['type'],
            'description': p.get('description'),
            'default': default,
            'required': p.get('required', False)
        }
    return parameters


def main():
    api_spec = get_openapi_spec()

    pack_bin_path = os.path.dirname(os.path.abspath(__file__))
    pack_root_path = os.path.dirname(pack_bin_path)
    pack_actions_path = os.path.join(pack_root_path, 'actions')
    env = Environment(loader=FileSystemLoader(pack_bin_path))
    template = env.get_template('template.jinja')

    # get all of the methods and parmaters from OpenAPI
    # will need to get the Default values from the Web API spec because
    # OpenAPI doesn't have them defined (yet)
    # https://github.com/slackapi/slack-api-specs/issues/40
    for path, http_methods in six.iteritems(api_spec['paths']):
        for http_method, op in six.iteritems(http_methods):
            method = path.replace('/', '')
            http_method = http_method.upper()
            http_ref_spec = get_spec_from_http_reference(method)
            params = get_params_from_openapi_operation(op, http_ref_spec['params'])
            if http_method != http_ref_spec['http_method']:
                print(("WARNING - http method is not the same for [{}] openapi={} http_ref={}"
                       " - defaulting to the preferred method from the HTTP reference.")
                      .format(method, http_method, http_ref_spec['http_method']))
                http_method = http_ref_spec['http_method']

            context = {
                'description': op['description'],
                'http_method': http_method,
                'method': method,
                'entry_point': 'run.py',
                'parameters': params,
            }

            # Positioning global param overrides before method params ensures that a
            # specific method override is prefered over a less specific global override

            # replace any global param overrides
            for p_override_key, p_override_value in six.iteritems(GLOBAL_PARAM_OVERRIDES):
                # check if the override param is in params
                if p_override_key in params:
                    # Loop through the keys:values that need to be overridden
                    for k, v in six.iteritems(p_override_value):
                        # override the current value
                        params[p_override_key][k] = v

            # replace any overrides in the context
            if method in METHOD_OVERRIDES:
                for override_key, override_value in six.iteritems(METHOD_OVERRIDES[method]):
                    if override_key == 'parameters':
                        for param_name, param_overrides in six.iteritems(override_value):
                            # check if the parameter already exists
                            if param_name in params:
                                # if the parameter exists, update the key/value pairs
                                for param_key, param_value in six.iteritems(param_overrides):
                                    params[param_name][param_key] = param_value
                            else:
                                # if the parameter doesn't exist, add it
                                params[param_name] = param_overrides

                    else:
                        context[override_key] = override_value

            # sort parameters by name, including any of the ones that might have been
            # adding during override processing
            context['parameters'] = sorted(context['parameters'].values(),
                                           key=lambda p: p['name'])

            # render our final jinja template
            rendered = template.render(**context)

            with open('{}.yaml'.format(os.path.join(pack_actions_path, method)), "w") as _f:
                _f.write(rendered + "\n")


if __name__ == "__main__":
    main()
