import requests
import six

from six.moves.urllib.parse import urlencode
from six.moves.urllib import parse as urlparse  # pylint: disable=import-error
urljoin = urlparse.urljoin

from st2common.runners.base_action import Action

BASE_URL = 'https://slack.com/api/'


class SlackAction(Action):

    def run(self, files=None, **kwargs):
        params = kwargs
        if params.get('token', None) is None:
            params['token'] = self.config['action_token']

        end_point = params['end_point']
        url = urljoin(BASE_URL, end_point)
        del params['end_point']

        http_method = params['http_method']
        del params['http_method']

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        for key in list(params.keys()):
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
                for k, v in six.iteritems(in_dict):
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
            if files:
                # we do NOT want Content-Type set in headers here because the content type
                # set above (application/x-www-form-urlencoded) will NOT work to
                # upload files. Instead we need requests to create a unique
                # Content-Type: multipart/formdata; boundary-----XYZ123
                # This Content-Type and boundary string is unique will be generated
                # automatically for us if we do not specify a Content-Type.
                # If we specify headers here with a Content-Type then file uploads
                # will not work and return mysterious errors
                headers.pop('Content-Type', None)

                # We're passing the params dict into the data parameter instead of
                # the URL encoded string 'data' from above, this is critical too
                # so that all of the additional parameters will be included as
                # multipart/formdata pieces. If you pass in the URL encoded data string
                # from above, this will put that single string in one form part of
                # the request and cause the request to fail. Instead what we want is
                # requests to create one multipart/formdata content section for each
                # parameters. By passing data=params (the dictionary) requests will
                # do what we want
                response = requests.post(url=url, headers=headers, data=params, files=files)
            else:
                response = requests.post(url=url, headers=headers, data=data)
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
