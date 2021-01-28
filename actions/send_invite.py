# used by users.admin.invite

import requests
from six.moves.urllib.parse import urlencode

from st2common.runners.base_action import Action

__all__ = [
    'SendInviteAction'
]


class SendInviteAction(Action):
    def run(self, email, channels, first_name, token, set_active, attempts):
        token = token if token else self.config['admin']['admin_token']
        set_active = set_active if set_active else self.config['admin'].get('set_active', True)
        attempts = attempts if attempts else self.config['admin'].get('attempts', 1)
        auto_join_channels = channels if channels \
            else self.config['admin'].get('auto_join_channels', "")
        url = "https://%s.slack.com/api/users.admin.invite" % \
            self.config['admin']['organization']
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = {
            'email': email.encode('utf-8'),
            'channels': " ".join(auto_join_channels),
            'token': token,
            'set_active': set_active,
            '_attempts': attempts
        }
        if first_name is not None:
            body['first_name'] = first_name.encode('utf-8')

        data = urlencode(body)
        response = requests.get(url=url,
                                headers=headers, params=data)
        results = response.json()

        if results['ok'] is True:
            return 'Invite successfully sent to %s. RESPONSE: %s' % \
                (email, results)
        else:
            failure_reason = ('Failed to send invite to %s: %s \
                              (status code: %s)' % (email, response.text,
                              response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return True
