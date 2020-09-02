from slack_base_action_test_case import SlackBaseActionTestCase
from users_filter_by import FilterBy

__all__ = [
    'TestActionSlackUserFilterByAction'
]


class TestActionSlackUserFilterByAction(SlackBaseActionTestCase):
    __test__ = False
    action_cls = FilterBy
