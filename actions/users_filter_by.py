# -*- coding: utf-8 -*-

'''
Lookup user by attibutes
'''

import six

from fnmatch import fnmatch
from run import SlackAction


class FilterBy(SlackAction):  # pylint: disable=too-few-public-methods
    '''
    Main class
    '''

    def run(self, **kwargs):
        '''
        Return a list of users
        '''

        users = []
        attrs = kwargs.pop('attributes')
        res = super(FilterBy, self).run(**kwargs)

        while res.get('response_metadata').get('next_cursor'):
            for user in res['members']:
                match = True
                for key, val in attrs.items():
                    if isinstance(val, six.string_types):
                        if not fnmatch(user.get(key, ''), val):
                            match = False
                    elif user.get(key) != val:
                        match = False

                if match:
                    users.append(user)

            kwargs.update({'cursor': res.get('response_metadata').get('next_cursor')})
            self.logger.debug(f"Next cursor: {kwargs.get('cursor')}")
            res = super(FilterBy, self).run(**kwargs)

        return users
