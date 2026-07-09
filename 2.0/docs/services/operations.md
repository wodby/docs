# Service operations

Service operations are workflows a service can expose for application maintenance, lifecycle hooks, recurring tasks,
data backup, and data import.

For the full manifest schema, see the [service template reference](template.md).

## Actions

Services can define actions that run commands in an app. Actions can be user-runnable from the app-service UI or run
automatically during deployment and upgrades. Each run creates a task with execution logs.

Actions run in the selected service workload. If an action does not specify `workload`, Wodby uses the service's
primary workload.

Deployment and upgrade actions run simultaneously unless dependencies are set between them.

### Action types

An action type defines how and when the action runs.

#### `button`

User-runnable action. Actions of this type are shown on the app service's `Actions` tab in the Wodby dashboard.
Each run creates a task; command output is available in the task logs.

#### `output`

User-runnable action. Actions of this type are shown on the app service's `Actions` tab. Running the action creates a
task; output is associated with the task logs and is not returned directly by the run operation.

#### `post_deploy`

Runs after every service deployment. If a deployment includes more than one service, the action runs only after all
deployments succeed. It can be limited to a specific build template.

#### `post_deploy_once`

Same as `post_deploy`, but runs only during the first deployment. It can be limited to a specific build template.

#### `post_upgrade`

Runs after an app instance is upgraded to a new stack revision.

#### `empty`

No-op action type used when a service needs to define an action placeholder without running a command. Empty actions are
not exposed as user-runnable app-service actions.

### App service actions

The app-service `Actions` tab shows only user-runnable service actions from the selected app service:

- `button`
- `output`

The dashboard does not derive runnable app-service actions from the raw service manifest. Wodby evaluates the app
service state and exposes only actions that can be considered for manual execution.

An app-service action can be disabled even when it appears in the tab. Actions are disabled when the app service or app
instance is not in a healthy `OK` state, and actions are not available for external or derivative app services.

Service actions are defined under the [`actions` section](template.md#actions) in a service template.

## Backups

Services can define data-backup behavior. There are two main backup methods.

### Simple files backup

Wodby creates a tar archive from the specified directory. The archive can optionally be gzipped.

The resulting archive is uploaded to the object-storage bucket configured through a connected storage integration.

### Backup through action

Wodby runs a Kubernetes job with the configured command or args override to create the backup archive. That job is
expected to place the archive in the specified volume path, after which Wodby uploads it to the configured
object-storage bucket.

Service backups are defined under the [`backups` section](template.md#backups) in a service template.

## Imports

Services can define data-import behavior. There are two main import methods.

### Simple files import

Wodby imports files directly into the running volume by unpacking the provided tar archive to the specified path.

This method is not transactional.

### Import through init volume

Wodby mounts the import archive into the init volume provided by the service, and a container performs the import during startup. This pattern is commonly used for databases.

This method is transactional. Wodby starts a copy of the app service with a new persistent volume. If the import succeeds, Wodby redeploys the service using the new volume that contains the imported data.

Service imports are defined under the [`imports` section](template.md#imports) in a service template.

## Cron schedules

Services can define cron schedules for recurring tasks. Each schedule includes a name, a command or argument override,
and a cron expression. Every run creates a task with execution logs.

Use standard five-field crontab syntax such as `0 * * * *`. Cron schedules cannot run more often than once per hour.

Cron schedules are defined under the [`cron` section](template.md#cron) in a service template.
