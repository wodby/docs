---
description: Run Slackin on Wodby 1 to let people join your Slack team, set the team name and token it needs, and read the stack changelog.
---

# Slackin stack

After deployment add the following environment variables:

* `SLACK_TEAM` – your Slack team name
* `SLACK_TOKEN` - generated token here: https://api.slack.com/custom-integrations/legacy-tokens

## Changelog

### 2.0.5

Bug fixes

### 2.0.0

- We now install [slackin-extended](https://github.com/emedvedev/slackin-extended)
- Rebased to Node 16

### 1.1.0

* Default [memory request](../config.md#resources) set to 16m

### 1.0.0

Initial release
