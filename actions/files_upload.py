from run import SlackAction

class FilesUploadAction(SlackAction):

    def run(self, **kwargs):
        if kwargs.get('token', None) is None:
            kwargs['token'] = self.config['action_token']

        # https://requests.readthedocs.io/en/master/user/quickstart/#post-a-multipart-encoded-file
        files = None
        if 'file' in kwargs['file']:
            # the name 'file' is hard coded because that's the name of the parameter
            # that the Slack API is expecting
            files = {'file': open(kwargs['file'], 'rb')}

        self._do_request(kwargs, files)
