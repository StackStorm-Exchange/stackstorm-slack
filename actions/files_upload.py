from st2common.runners.base_action import Action
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class FilesUploadAction(Action):

    def run(self, **kwargs):
        token = kwargs.get('token') if kwargs.get('token') else self.config['action_token']
        client = WebClient(token=token)
        if 'file_path' in kwargs and kwargs['file_path']:
            if 'file' in kwargs and kwargs['file']:
                raise RuntimeError('Passing in "file" and "file_path" at the same time is'
                                   ' not supported. If you would like to have this action'
                                   ' read the file from the filesystem and upload it for you'
                                   ' then use the "file_path" parameter. Otherwise, if you'
                                   ' would like to read the file yourself and pass in the data'
                                   ' then use the "file" parameter set to the content.')
        try:
            file = kwargs['file'] if kwargs['file'] else kwargs['file_path']
            response = client.files_upload_v2(
                filename=kwargs['filename'],
                file=file,
                content=kwargs['content'],
                title=kwargs['title'],
                channel=kwargs['channels'],
                initial_comment=kwargs['initial_comment'],
                thread_ts=kwargs['thread_ts'],
            )
            assert response['file']
            return response.get('file', {}).get('name')
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            return False, e.response['error']