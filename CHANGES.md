# Change Log

# 0.12.8

- Don't require ``post_message_action`` config option to be set when ``webhook_url`` parameter is
  provided when calling ``slack.post_message`` action.

# 0.12.7

- fix `attachments` parameter type in sensor.
- update `jinja` dependency to 2.10.1+
- use upstream `slackclient` package

# 0.12.6

- Fix `text` parameter in `chat.update` to be `required: false`, same as `chat.postMessage`. `text` only required when `attachments` is `None` 
- Update icon to new rebranded Slack icon 

# 0.12.5

- Bump allowed `requests()` version, remove httplib

# 0.12.4

- Added `is_bot` attribute to the user payload in `slack_sensor` sensor.

# 0.12.3

- Added `attachments` as part of the `slack_sensor` sensor payload.

# 0.12.2

- Added the option `allow_bot_messages` in the `slack_sensor` sensor.

# 0.12.1

- Fix `text` parameter to be optional in `chat.postMessage` action.

# 0.12.0

- Handling of cyrillic and special symbols in `run.py` through adding utf-8 encoding.

# 0.11.0

- All actions now uses preferred HTTP method mentioned in official API reference.

# 0.10.4

- Sync with the latest Slack API.
- Modified:
    - `files.info`
    - `groups.list`
    - `mpim.list`
    - `reactions.list`
    - `stars.list`
        - Add optional parameters: `cursor`, `limit`

# 0.10.3

- Sync with the latest Slack API.
- Added:
    - `apps.permissions.info`
    - `apps.permissions.request`
    - `apps.permissions.resources.list`
    - `apps.permissions.scopes.list`
    - `apps.permissions.users.list`
    - `apps.permissions.users.request`
    - `chat.getPermalink`
    - `chat.postEphemeral`
    - `conversations.archive`
    - `conversations.close`
    - `conversations.create`
    - `conversations.history`
    - `conversations.info`
    - `conversations.invite`
    - `conversations.join`
    - `conversations.kick`
    - `conversations.leave`
    - `conversations.list`
    - `conversations.members`
    - `conversations.open`
    - `conversations.rename`
    - `conversations.replies`
    - `conversations.setPurpose`
    - `conversations.setTopic`
    - `conversations.unarchive`
    - `dialog.open`
    - `migration.exchange`
    - `oauth.token`
    - `users.conversations`
    - `users.lookupByEmail`
- Modified:
    - `oauth.access`
        - Add `single_channel` optional parameter

# 0.10.2

* Add thread_ts parameter to `files.upload` action.

# 0.10.1

* Fix to use POST in `files.upload` action so that it can upload larger content.

# 0.10.0

* Fortify `send_invite.py` to better handle optional parameters.

# 0.9.0

- Add `secret: true` for `webhook_url` in config.schema.yaml.

# 0.8.0

- Added custom `users_filter_by` action.

# 0.7.0

- Enforce default values to be a string type in YAML action definitions.
- Update actions according to latest Slack API changes.

# 0.6.5

- Remove `groups.close` action that is no longer available among Slack API methods.

# 0.6.2

- Remove required flag from `action_token` since other sections could be configured without relying on it.

# 0.4.0

- Updated action `runner_type` from `run-python` to `python-script`

# 0.3.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
