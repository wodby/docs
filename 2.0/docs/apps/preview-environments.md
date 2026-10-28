# Preview environments

A preview environment is a temporary [app environment](environments.md) that Wodby creates for a pull request. When a
pull request is opened against the branch your base environment follows, Wodby copies that environment, builds the
pull request branch, seeds the services you selected with data from the base environment, and posts the result back to
the pull request. Every push to the pull request rebuilds the preview, and Wodby deletes it when the pull request is
closed or merged, or after it has been idle for a configurable number of days.

Preview environments are disabled by default and configured per app.

## Prerequisites

- The base environment must be a standard environment, not a [development workspace](workspaces.md), with at least one
  enabled service connected to a Git branch through a [GitHub](../providers/github.md) integration. Pull requests are
  matched against that branch, so an environment following `main` creates previews for pull requests into `main`.
- The GitHub App installation must be allowed to read pull requests, create commit statuses, and comment on pull
  requests. GitHub asks the installation owner to approve these permissions when they are missing. Until they are
  approved, previews are still created, but the pull request receives no status or comment. See
  [GitHub](../providers/github.md#preview-environments).
- The base environment must use `Public` [App access](access.md). Protected environments are not supported yet.
- Database services of the base environment must run as containers in the environment. Environments that use an
  existing database server are not supported yet.
- The cluster of the base environment must allow the environment type chosen for previews. See
  [Environment types](environment-types.md).

GitLab and Bitbucket repositories do not trigger preview environments yet.

## Enabling preview environments

For a new application, open the `Preview environments` section in step 4 of the
[new application form](index.md#step-4) and set `Pull request previews` to `Enabled`. The environment you are creating
becomes the base environment. The option is available when a service has a build source and the deployment mode is
CI/CD. You choose which services are seeded with data after the application is created.

For an existing application, open `Apps > [App] > Settings > Preview environments`. You need permission to modify the
app.

## Settings

| Setting | Description |
| --- | --- |
| `Pull request previews` | Turns preview environments on or off for the app. Turning them off does not delete existing previews; they are still removed when their pull requests close. |
| `Base environment` | The environment whose configuration is copied into every preview and whose services provide seed data. Only standard environments of the app are offered. |
| `Environment type` | The [environment type](environment-types.md) of created previews. `feature` is the default; `prod` is not allowed. |
| `Draft pull requests` | Whether draft pull requests get previews. Disabled by default; a preview is created when the draft is marked ready for review. |
| `Concurrent previews` | The maximum number of preview environments the app keeps at the same time, up to 50. Pull requests beyond the limit are skipped until a preview is deleted. The default is 5. |
| `Idle expiry (days)` | Deletes a preview whose pull request had no activity for this many days. The default is 7; `0` disables idle expiry. |
| `Seed data` | Base environment services that support both imports and backups. Select a service to restore a fresh backup of it into every new preview, and choose the import and backup when the service offers more than one. |

Seeding a service requires a [backup preset](backups.md) for the chosen backup in the base environment. Services
without one are listed with a `No backup preset` tag and cannot be selected until a preset exists; the tag links to the
base environment's presets.

If seeding a selected service is not possible when a preview is created, the preview is still created and that service
starts without data. This happens when the preset was deleted, or the service was removed, disabled, or not in `OK`
status in the base environment. Wodby reports it on the pull request (see [Pull request feedback](#pull-request-feedback)).
Deleting a backup preset that previews seed from finishes with a warning that explains this.

Changes to these settings apply to previews created afterwards. Existing previews keep running until their pull request
closes or they expire.

## What a preview contains

Each preview is created from the base environment at the moment the pull request is picked up:

- Service configuration is copied: enabled services and versions, settings, environment variables, volume sizes,
  integrations, cron schedules, and service links. Secret values are copied as well.
- The service connected to the pull request repository follows the pull request branch instead of the base branch.
- Container database services get their own database. Preview environments never share a database with the base
  environment.
- Selected services are seeded from a fresh backup of the base environment taken at creation time. The backup is
  restored during the preview's first deployment, so a large database delays the first successful deployment.
- Custom domains, TLS certificates, HTTP authentication, and Application Access are not copied. The preview is reached
  through its generated technical domain.

The environment machine name is `pr-<number>`, the title shows the pull request number and title, and the technical
domain follows the usual `*.pr-<number>.[app-name].[org-name].wodby.app` pattern. Previews count toward app-service
plan usage like any other environment while they exist.

## Lifecycle

| Event | Result |
| --- | --- |
| Pull request opened, reopened, or marked ready for review | A preview is created when the pull request targets the base environment's branch and no preview exists yet. A push to a pull request without a preview also creates one, for example after enabling previews for an open pull request. |
| Push to the pull request branch | The preview is rebuilt and redeployed with the new commit. A push that arrives while a deployment is running is built after that deployment finishes. |
| Pull request closed or merged | The preview is deleted. If deletion cannot start, for example while a build is running, Wodby retries it automatically. |
| No activity for the idle expiry period | The preview is deleted. |
| Pull request from a fork | No preview is created. Forks could run untrusted code with the app's configuration. |
| Draft pull request | No preview is created unless `Draft pull requests` is enabled. |
| Concurrent preview limit reached | The pull request is skipped and gets a failed `wodby/preview` status. It gets a preview on its next push once a preview has been deleted. |

Automatic preview deletion is not blocked by the organization's [termination protection](../org.md#termination-protection).
You can also delete a preview manually from the app's environments list; the next push to the pull request creates a
new one.

## Pull request feedback

Wodby reports each preview deployment to the pull request as a `wodby/preview` commit status on the commit it built:
`pending` while the environment is being created, then `success` or `failure` with a link to the preview. After the
first successful deployment, Wodby posts one comment on the pull request with the preview URL. Later deployments only
update the commit status.

A deployment that did not build the pull request commit, such as a configuration-only redeploy, does not change the
status.

When Wodby cannot create a preview for a pull request, it sets the `wodby/preview` status to `failure` with the
reason, for example that the base environment is not in `OK` status or that the concurrent preview limit is reached.
The next push to the pull request tries again.

When a preview is created but some selected services could not be seeded, Wodby also sets a `wodby/preview-data`
status to `failure` that names the service and the reason, or the number of affected services. The preview itself
works; those services start without data. Fix the cause, such as adding the missing backup preset, then delete the
preview and push to the pull request to create it again with data.

## Finding previews in the dashboard

Preview environments appear in `Apps > [App] > Environments` with a `PR #<number>` tag and can be opened like any other
environment. Their creation, deployments, and deletion are listed under the app's `Tasks` tab, where the creation task is
titled with the pull request number.

If a pull request does not get a preview, check the `wodby/preview` status on the pull request for the reason. Also check
that previews are enabled for the app, that the pull request targets the branch the base environment follows, and that
it is not a draft or from a fork.

## Related pages

- [App environments](environments.md)
- [Applications overview](index.md)
- [Backups](backups.md)
- [Imports](imports.md)
- [GitHub](../providers/github.md)
