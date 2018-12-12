import json

try:
    from six.moves.urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from st2common.runners.base_action import Action

__all__ = [
    'PostMessageAction'
]


class PostMessageAction(Action):
    def run(self, message, username=None, icon_emoji=None, channel=None,
            disable_formatting=False, webhook_url=None):
        config = self.config['post_message_action']
        username = username if username else config['username']
        icon_emoji = icon_emoji if icon_emoji else config.get('icon_emoji', None)
        channel = channel if channel else config.get('channel', None)
        webhook_url = webhook_url if webhook_url else config.get('webhook_url', None)

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = {
            'username': username,
            'icon_emoji': icon_emoji,
            'text': message
        }

        if channel:
            body['channel'] = channel

        if disable_formatting:
            body['parse'] = 'none'

        if webhook_url:
            body['webhook_url'] = webhook_url

        data = {'payload': json.dumps(body)}
        data = urlencode(data)
        response = requests.post(url=webhook_url,
                                 headers=headers, data=data)

        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            self.logger.info('Message successfully posted')
        else:
            failure_reason = ('Failed to post message: %s (status code: %s)' %
                              (response.text, response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return True
