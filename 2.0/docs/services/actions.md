# Service actions

## Overview

Services can define actions that run commands in an app. Actions can be user-runnable from the app-service UI or run
automatically during deployment and upgrades. Each run creates a task with execution logs.

Actions run in the selected service workload. If an action does not specify `workload`, Wodby uses the service's
primary workload.

Deployment and upgrade actions run simultaneously unless dependencies are set between them.

## Types

An action type defines how and when the action runs.

### `button`

User-runnable action. Actions of this type are shown on the app service's `Actions` tab in the Wodby dashboard.
Each run creates a task; command output is available in the task logs.

### `output`

User-runnable action. Actions of this type are shown on the app service's `Actions` tab. Running the action creates a
task; output is associated with the task logs and is not returned directly by the run operation.

### `post_deploy`

Runs after every service deployment. If a deployment includes more than one service, the action runs only after all
deployments succeed. It can be limited to a specific build template.

### `post_deploy_once`

Same as `post_deploy`, but runs only during the first deployment. It can be limited to a specific build template.

### `post_upgrade`

Runs after an app instance is upgraded to a new stack revision.

### `empty`

No-op action type used when a service needs to define an action placeholder without running a command. Empty actions are
not exposed as user-runnable app-service actions.

## App service actions

The app-service `Actions` tab shows only user-runnable service actions from the selected app service:

- `button`
- `output`

The dashboard does not derive runnable app-service actions from the raw service manifest. Wodby evaluates the app
service state and exposes only actions that can be considered for manual execution.

An app-service action can be disabled even when it appears in the tab. Actions are disabled when the app service or app
instance is not in a healthy `OK` state, and actions are not available for external or derivative app services.

## Template

Service actions are defined under the [`actions` section](template.md#actions) in a service template.
