import mock
import responses

from slack_base_action_test_case import SlackBaseActionTestCase
from run import SlackAction


__all__ = [
    'TestActionSlackRunAction'
]

VALID_REQUEST = {'token': 'test_token',
                 'end_point': 'test',
                 'http_method': 'POST',
                 'channel': 'ABCD1234',
                 'as_user': 'true',
                 'text': 'message'}

# Dictionary Comprehension - Removes the key 'token'
VALID_REQUEST_NO_TOKEN = {i: VALID_REQUEST[i] for i in VALID_REQUEST if i != 'token'}

SUCCESS_RESPONSE = {'ok': True,
                    'channel': 'ABCD1234',
                    'message': {
                        'text': 'message'}}


class TestActionSlackRunAction(SlackBaseActionTestCase):
    __test__ = True
    action_cls = SlackAction

    # Check that the action will run with various combinations of
    # token in params and/or config.
    @mock.patch('run.requests.post')
    def test_run_action_blank_config_with_token(self, mock_connection):
        action = self.get_action_instance(self.config_blank)

        action.run(**VALID_REQUEST)

    @mock.patch('run.requests.post')
    def test_run_action_blank_config_no_token(self, mock_connection):
        action = self.get_action_instance(self.config_blank)

        self.assertRaises(Exception, action.run, **VALID_REQUEST_NO_TOKEN)

    @mock.patch('run.requests.post')
    def test_run_action_full_config_with_token(self, mock_connection):
        action = self.get_action_instance(self.config_token)

        action.run(**VALID_REQUEST)

    @mock.patch('run.requests.post')
    def test_run_action_full_config_no_token(self, mock_connection):
        action = self.get_action_instance(self.config_token)

        action.run(**VALID_REQUEST_NO_TOKEN)

    # Run the action with a valid request, assuming a successful response
    @responses.activate
    def test_post_message_success(self):
        MOCK_URL = 'https://slack.com/api/test'
        responses.add(responses.POST, MOCK_URL, json=SUCCESS_RESPONSE, status=200)

        action = self.get_action_instance(self.config_blank)

        result = action.run(**VALID_REQUEST)
        self.assertEqual(result, SUCCESS_RESPONSE)

    # Run the action with a valid request, assuming a fail response
    @responses.activate
    def test_post_message_fail(self):
        MOCK_URL = 'https://slack.com/api/test'
        RESPONSE = {'ok': False, 'error': 'error message'}
        responses.add(responses.POST, MOCK_URL, json=RESPONSE, status=200)

        action = self.get_action_instance(self.config_blank)
        self.assertRaises(Exception, action.run, **VALID_REQUEST)
