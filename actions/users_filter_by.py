# -*- coding: utf-8 -*-

'''
Lookup user by attibutes
'''

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

        for user in res['members']:
            match = True
            for key, val in attrs.items():
                if isinstance(val, basestring):
                    if not fnmatch(user.get(key, ''), val):
                        match = False
                elif user.get(key) != val:
                    match = False

            if match:
                users.append(user)

        return users
