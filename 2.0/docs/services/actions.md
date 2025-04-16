# Service actions

## Overview

Service can define an action that will execute an operation in an app. When an action executed it will run a kubernetes job with the provided overridden args/commands and optionally privileged permissions. A task containing the logs of the execution will be created.

Service with multiple actions will run all actions simultaneously unless there are action with dependency order specified.

## Types

Action's type defines how and when the action will be executed.

### `button`

Action's of this type will be shown as a button in Wodby dashboard. 

### `post_deploy`

Post-deployment action that will run after every service deployment. If deploy contains more than one service, the action will run only when all deployments succeeded. Can be limited to run only when a specific build source templates selected. 

### `post_deploy_once`

Same as `post_deploy` but run only during first deployment. Can be limited to run only when a specific build source templates selected.

### `post_upgrade`

Post-upgrade action

### `output`

Action produces output that will be shown in Wodby dashboard. 

## Template 

Service actions defined under [`actions` section](template.md#annotations) in a service template.
