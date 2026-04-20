# Service actions

## Overview

Services can define actions that run commands in an app. Actions can be shown as buttons in the UI or run
automatically during deployment and upgrades. Each run creates a task with execution logs.

If a service defines multiple actions, they run simultaneously unless dependencies are set between them.

## Types

An action type defines how and when the action runs.

### `button`

Actions of this type are shown as buttons in the Wodby dashboard.

### `post_deploy`

Runs after every service deployment. If a deployment includes more than one service, the action runs only after all
deployments succeed. It can be limited to a specific build template.

### `post_deploy_once`

Same as `post_deploy`, but runs only during the first deployment. It can be limited to a specific build template.

### `post_upgrade`

Runs after a stack upgrade.

### `output`

Produces output that is shown in the Wodby dashboard.

## Template

Service actions are defined under the [`actions` section](template.md#actions) in a service template.
