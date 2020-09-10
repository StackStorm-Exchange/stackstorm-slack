from slack_base_action_test_case import SlackBaseActionTestCase
from send_invite import SendInviteAction

__all__ = [
    'TestActionSlackSendInviteAction'
]


class TestActionSlackSendInviteAction(SlackBaseActionTestCase):
    __test__ = False
    action_cls = SendInviteAction
