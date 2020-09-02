from slack_base_action_test_case import SlackBaseActionTestCase
from files_upload import FilesUploadAction

__all__ = [
    'TestActionSlackFilesUploadAction'
]


class TestActionSlackFilesUploadAction(SlackBaseActionTestCase):
    __test__ = False
    action_cls = FilesUploadAction
