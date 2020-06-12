from run import SlackAction


class FilesUploadAction(SlackAction):

    def run(self, **kwargs):
        if kwargs.get('token', None) is None:
            kwargs['token'] = self.config['action_token']

        # https://requests.readthedocs.io/en/master/user/quickstart/#post-a-multipart-encoded-file
        files = None
        if 'file_path' in kwargs:
            if 'file' in kwargs:
                raise RuntimeError('Passing in "file" and "file_path" at the same time is'
                                   ' not supported. If you would like to have this action'
                                   ' read the file from the filesystem and upload it for you'
                                   ' then use the "file_path" paramter. Otherwise, if you'
                                   ' would like to read the file yourself and pass in the data'
                                   ' then use the "file" paramter set to the content.')
            # the name 'file' is hard coded because that's the name of the parameter
            # that the Slack API is expecting
            files = {'file': open(kwargs['file'], 'rb')}

        self._do_request(kwargs, files)
