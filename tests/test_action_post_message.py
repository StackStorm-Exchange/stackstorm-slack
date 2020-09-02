from slack_base_action_test_case import SlackBaseActionTestCase
from post_message import PostMessageAction

__all__ = [
    'TestActionSlackPostMessageAction'
]


class TestActionSlackPostMessageAction(SlackBaseActionTestCase):
    __test__ = False
    action_cls = PostMessageAction
