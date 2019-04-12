from st2common.runners.base_action import Action
import requests
import six

from six.moves.urllib.parse import urlencode
from six.moves.urllib import parse as urlparse  # pylint: disable=import-error
urljoin = urlparse.urljoin


BASE_URL = 'https://slack.com/api/'


class SlackAction(Action):

    def run(self, **kwargs):
        if kwargs.get('token', None) is None:
            kwargs['token'] = self.config['action_token']

        return self._do_request(kwargs)

    def _do_request(self, params):
        end_point = params['end_point']
        url = urljoin(BASE_URL, end_point)
        del params['end_point']

        http_method = params['http_method']
        del params['http_method']

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        for key in params.keys():
            if params[key] is None:
                del params[key]

        def encode_obj(in_obj):

            def encode_list(in_list):
                out_list = []
                for el in in_list:
                    out_list.append(encode_obj(el))
                return out_list

            def encode_dict(in_dict):
                out_dict = {}
                for k, v in in_dict.iteritems():
                    out_dict[k] = encode_obj(v)
                return out_dict

            if isinstance(in_obj, six.text_type):
                return in_obj.encode('utf-8')
            elif isinstance(in_obj, list):
                return encode_list(in_obj)
            elif isinstance(in_obj, tuple):
                return tuple(encode_list(in_obj))
            elif isinstance(in_obj, dict):
                return encode_dict(in_obj)

            return in_obj

        data = urlencode(encode_obj(params))

        if http_method == 'POST':
            response = requests.post(url=url,
                                     headers=headers, data=data)
        elif http_method == 'GET':
            response = requests.get(url=url,
                                    headers=headers, params=data)
        else:
            failure_reason = ('Failed to perform action %s: Invalid HTTP method: %s' % (
                end_point, http_method))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        results = response.json()
        if not results['ok']:
            failure_reason = ('Failed to perform action %s: %s \
                              (status code: %s)' % (end_point, response.text,
                              response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return results
