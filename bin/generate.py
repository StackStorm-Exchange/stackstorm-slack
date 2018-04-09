#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Generate YAML files for ST2 actions based on Slack API methods
'''


# StdLib
import os
import re

# External
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import requests


def main():  # pylint: disable=too-many-locals
    '''
    Parse web docs for Slack API methods and write YAML actions
    '''

    cwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(os.path.dirname(cwd), 'actions')
    env = Environment(loader=FileSystemLoader(cwd))

    template = env.get_template('template.jinja')

    # TODO: Scrape list of methods from https://api.slack.com/methods
    # For now, just hardcode the list.
    methods = [
        'api.test',
        'auth.revoke',
        'auth.test',
        'bots.info',
        'channels.archive',
        'channels.create',
        'channels.history',
        'channels.info',
        'channels.invite',
        'channels.join',
        'channels.kick',
        'channels.leave',
        'channels.list',
        'channels.mark',
        'channels.rename',
        'channels.replies',
        'channels.setPurpose',
        'channels.setTopic',
        'channels.unarchive',
        'chat.delete',
        'chat.meMessage',
        'chat.postMessage',
        'chat.unfurl',
        'chat.update',
        'dnd.endDnd',
        'dnd.endSnooze',
        'dnd.info',
        'dnd.setSnooze',
        'dnd.teamInfo',
        'emoji.list',
        'files.comments.add',
        'files.comments.delete',
        'files.comments.edit',
        'files.delete',
        'files.info',
        'files.list',
        'files.revokePublicURL',
        'files.sharedPublicURL',
        'files.upload',
        'groups.archive',
        'groups.create',
        'groups.createChild',
        'groups.history',
        'groups.info',
        'groups.invite',
        'groups.kick',
        'groups.leave',
        'groups.list',
        'groups.mark',
        'groups.open',
        'groups.rename',
        'groups.replies',
        'groups.setPurpose',
        'groups.setTopic',
        'groups.unarchive',
        'im.close',
        'im.history',
        'im.list',
        'im.mark',
        'im.open',
        'im.replies',
        'mpim.close',
        'mpim.history',
        'mpim.list',
        'mpim.mark',
        'mpim.open',
        'mpim.replies',
        'oauth.access',
        'pins.add',
        'pins.list',
        'pins.remove',
        'reactions.add',
        'reactions.get',
        'reactions.list',
        'reactions.remove',
        'reminders.add',
        'reminders.complete',
        'reminders.delete',
        'reminders.info',
        'reminders.list',
        'rtm.connect',
        'rtm.start',
        'search.all',
        'search.files',
        'search.messages',
        'stars.add',
        'stars.list',
        'stars.remove',
        'team.accessLogs',
        'team.billableInfo',
        'team.info',
        'team.integrationLogs',
        'team.profile.get',
        'usergroups.create',
        'usergroups.disable',
        'usergroups.enable',
        'usergroups.list',
        'usergroups.update',
        'usergroups.users.list',
        'usergroups.users.update',
        'users.deletePhoto',
        'users.getPresence',
        'users.identity',
        'users.info',
        'users.list',
        'users.setActive',
        'users.setPhoto',
        'users.setPresence',
        'users.profile.get',
        'users.profile.set',
    ]

    for method in methods:
        print method
        page = requests.get("https://api.slack.com/methods/" + method)

        soup = BeautifulSoup(page.text, "lxml")
        msec = soup.find("section", attrs={"data-tab": "docs"})
        description = msec.find("p").text
        table = msec.find("table", "arguments full_width")
        rows = table.find_all("tr")
        parameters = []
        for row in rows:
            cols = row.find_all("td")
            if cols:
                name = cols[0].text

                default = ""
                matches = re.match(r'.*default=(.+)$', cols[2].text, re.M | re.I)
                if matches:
                    default = matches.group(1)

                req = "false"
                if "Required" in cols[2].text:
                    if name != "token":
                        req = "true"
                parameters.append((name, default, req))

        rendered = template.render(description=description, method=method,
                                   parameters=parameters)
        with open('{}.yaml'.format(os.path.join(path, method)), "wb") as _f:
            _f.write(rendered + "\n")


if __name__ == "__main__":
    main()
