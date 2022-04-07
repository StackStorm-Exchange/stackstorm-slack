# Change Log

# 2.2.0

* Added action `post_attachment`

# 2.1.0

* Upgrade lxml dependency from 3.8.0 to 4.6.5

# 2.0.5

* Add `blocks` from slack message to sensor `payload`

# 2.0.4

* Add support for `conversations.info` slack method  as `groups.info` and
  `channels.info` were deprecated.
* Fix a bug in `SlackSensor._api_call`. There is no need to `json.loads` the
  result as slackclient 1.3.1 already parses the json.

# 2.0.3

* Add support for Slack apps created post Feb. 24, 2021 that no longer support
  tokens being passed in the url

# 2.0.2

* Make the `http_method` parameter to `files.upload` not required, and make it
  an enum parameter since only POST and GET are supported anyway.

# 2.0.1

* Remove default value from `slack.files.upload` `file_path` parameter

# 2.0.0

* Drop Python 2.7 support

# 1.1.1

### Fixes
- Extended override logic in `./bin/generate_openapi.py` to allow for global param overrides. token[required] is now forced to `false` #60
- Fix python 2.7/3.6 compatibility for ./actions/run.py #63 #58 #59

### Additions
- CODEOWNER file
- Basic unit testing and structure for expanded unit testing

# 1.1.0

- Added the ability for `slack.files.upload` to upload a file from the filesystem
  using the new `file_path` parameter. See the README for more details.
- Fixed bugs in `slack.files.upload` where the upload wasn't sending data via the API
  in the correct format, causing the uplaods to fail.

  Contributed by Nick Maludy (@nmaludy)

# 1.0.0

- Updated all actions to latest API spec as of 2020-06-11.
- Converted action auto-generator to using both the OpenAPI spec and the HTTP reference.
- Removed old action auto-generator so we can develop on a common tool.

  Contributed by Nick Maludy (@nmaludy)

# 0.13.0

- Various improvements to the ``slack.post_message`` action:
  - Make ``icon_emoji`` config option and parameter option. If it's not specified, it will now
    use server-side default.
  - Add new ``icon_url`` parameter to the action.
  - Make ``post_message_action.webhook_url`` config optional. This value can either be specified in
   the config or overriden on per action invocation basis.

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
