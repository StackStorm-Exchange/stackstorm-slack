# Change Log

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
