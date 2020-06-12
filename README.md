# Slack Integration Pack

Pack which allows integration with [Slack](https://slack.com/) service.

## Configuration

Copy the example configuration in [`slack.yaml.example`](./slack.yaml.example)
to `/opt/stackstorm/configs/slack.yaml` and edit as required.

* ``post_message_action.webhook_url`` - Webhook URL.
* ``post_message_action.channel`` - Channel to send the message to (e.g.
  `#mychannel`). If not specified, messages will be sent to the channel which
  is selected when configuring a webhook.
* ``post_message_action.username`` - Default name of the user under which the
  messages will be posted. This setting can be overridden on per action basis.
* ``post_message_action.icon_emoji`` - Default icon of the user under which the
  messages will be posted. This setting can be overridden on per action basis.
  If not provided, default value which is selected when configuring a webhook
  is used.
* ``sensor.token`` - Authentication token used to authenticate against Real
  Time Messaging API.
* ``sensor.strip_formatting`` - By default, Slack automatically parses URLs, images,
  channels, and usernames. This option removes formatting and only returns the raw
  data from the client (URL only today)
* ``sensor.allow_bot_messages`` - Allow the sensor to be triggered by bot messages without the as_user attribute. 
  Defaults to false in order to provide backwards compatibility 

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

### Obtaining a Webhook URL

To configure a webhook and obtain a URL, go to
https://[your company].slack.com/services/new/incoming-webhook, select a
channel you would like the messages to be posted to and click on "Add
Incoming WebHooks Integration" button.

![Step 1](/etc/slack_generate_webhook_url_1.png)

On the next page you will find an automatically generated webhook URL.

![Step 2](/etc/slack_generate_webhook_url_2.png)

### Obtaining Auth Token

To obtain a token for a production use, you should follow the instructions on
the following page - [OAuth - User
Authentication](https://api.slack.com/docs/oauth).

For testing purposes, you can use the same token as your browser based client
uses.

This is a lot simpler than going through the whole oAuth flow, but because of
the obvious security reasons and a temporary natural of the token, you should
only use that token for testing and debugging

To do that, navigate to your Slack instance (e.g. mycompany.slack.com),
open Chrome developer console, go to `Network` tab, filter on `XHR` requests
and refresh the page. Find a request to `file.list` or a similar endpoint
and in the right page, under the `Requests Payload` section you will see
an item identified as `Content-Disposition: form-data; name="token"`.  This
will contain the token that your client uses to authenticate.

![Chrome developer console](/etc/slack_obtain_test_auth_token.png)

## Sensors

### SlackSensor

Slack sensor monitors Slack for activity and dispatches a trigger for each
message which is posted to a channel.

#### slack.message trigger

Example trigger payload:

```json
{
    "user": {
        "first_name": "Tomaz",
        "last_name": "Muraus",
        "is_owner": false,
        "name": "kami",
        "real_name": "Tomaz Muraus",
        "is_admin": false,
        "id": "U0CCCCC"
    },
    "channel": {
        "topic": "",
        "id": "C0CCCCCC",
        "name": "test"
    },
    "timestamp": 1419164091,
    "timestamp_raw": "1419164091.00005",
    "text": "This is a test message."
}
```

## Actions

The following two actions are provided by the Slack pack.

* ``post_message`` - Post a message to the specified channel using an incoming webhook.
* ``users.admin.invite`` - Send an invitation to join a Slack Org.
* ``users_filter_by`` - List users in a Slack team matching certain creterias.

All other actions are as documented on the [Slack API Methods](https://api.slack.com/methods) page.

Let's consider the [chat.postMessage](https://api.slack.com/methods/chat.postMessage)
method. You'll notice that it lists 14 parameters. Three of the 14 parameters are required, and
the remainder are optional.

You can also list the actions available in st2 using `st2 action list -p slack`, and get help on
each action using `st2 action get slack.<action>`, where `<action>` is the name of an action. Given
our above example action:

```
root@c603fc2f139a:/opt/stackstorm/packs.dev/slack# st2 action list -p slack
+-------------------------------+-------+--------------------------------------------------------------+
| ref                           | pack  | description                                                  |
+-------------------------------+-------+--------------------------------------------------------------+
...
| slack.chat.meMessage          | slack | This method sends a me message to a channel from the calling |
|                               |       | user.                                                        |
| slack.chat.postMessage        | slack | This method posts a message to a public channel, private     |
|                               |       | channel, or direct message/IM channel (Allows posting to any |
|                               |       | slack channel using the unique webhook url).                       |
| slack.chat.unfurl             | slack | This method attaches Slack app unfurl behavior to a          |
|                               |       | specified and relevant message.                              |
...
+-------------------------------+-------+--------------------------------------------------------------+
root@c603fc2f139a:/opt/stackstorm/packs.dev/slack# st2 action get slack.chat.postMessage
+-------------+--------------------------------------------------------------+
| Property    | Value                                                        |
+-------------+--------------------------------------------------------------+
| id          | 596d3f26cf8580020317b9ca                                     |
| uid         | action:slack:chat.postMessage                                |
| ref         | slack.chat.postMessage                                       |
| pack        | slack                                                        |
| name        | chat.postMessage                                             |
| description | This method posts a message to a public channel, private     |
|             | channel, or direct message/IM channel.                       |
| enabled     | True                                                         |
| entry_point | run.py                                                       |
| runner_type | python-script                                                |
| parameters  | {                                                            |
|             |     "username": {                                            |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "thread_ts": {                                           |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "attachments": {                                         |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "unfurl_links": {                                        |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "end_point": {                                           |
|             |         "default": "chat.postMessage",                       |
|             |         "type": "string",                                    |
|             |         "immutable": true                                    |
|             |     },                                                       |
|             |     "link_names": {                                          |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "unfurl_media": {                                        |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "parse": {                                               |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "token": {                                               |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "text": {                                                |
|             |         "required": true,                                    |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "icon_emoji": {                                          |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "as_user": {                                             |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "icon_url": {                                            |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "channel": {                                             |
|             |         "required": true,                                    |
|             |         "type": "string"                                     |
|             |     },                                                       |
|             |     "reply_broadcast": {                                     |
|             |         "required": false,                                   |
|             |         "type": "string"                                     |
|             |     }                                                        |
|             | }                                                            |
| notify      |                                                              |
| tags        |                                                              |
+-------------+--------------------------------------------------------------+
```

Notice how there are 15 parameters. The extra one is "end_point", which is used by run.py
to construct the end point URL.


### Uploading files with slack.files.upload

The action `slack.files.upload` is able to upload files to slack, such as pictures. 
This action works a bit different than other actions in that the `file_path` parameter
accepts a path to a file on the local filesystem. This path *must* be
accessible from the the `st2actionrunner` executing the action.
The `st2actionrunner` will open up the file path, read the contents and then upload
this data to Slack as part of the action run.

Example:

```shell
st2 run slack.files.upload file_path=/opt/data/mycoolimage.png filename=mycoolimage.png
```

If this is not desirabile and you would rather read the file or pass the data
yourself, this can be accomplished using the `file` or `content` parameters which both
accept raw data that will be uploaded.


## Developer Reference

### How to auto-generate actions

If you're a pack developer working on this pack and want to auto-generate / update
the actions here, please see [bin/README.md](bin/README.md)
