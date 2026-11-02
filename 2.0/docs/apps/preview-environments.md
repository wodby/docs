# Preview environments

A preview environment is a temporary [app environment](environments.md) that Wodby creates for a pull request. When a
pull request is opened against the branch your base environment follows, Wodby copies that environment, builds the
pull request branch, seeds the services you selected with data from the base environment, and posts the result back to
the pull request. With Wodby CI, every push to the pull request rebuilds the preview. With a third-party CI system, your
pipeline starts the builds. Wodby deletes the preview when the pull request is closed or merged, or after it has been
idle for a configurable number of days.

Preview environments are disabled by default and configured per app. They work with GitHub, GitLab, and Bitbucket. This
page says pull request for what GitLab calls a merge request.

## Prerequisites

- The base environment must be a standard environment, not a [development workspace](workspaces.md), with at least one
  enabled service connected to a Git branch through a [GitHub](../providers/github.md),
  [GitLab](../providers/gitlab.md), or [Bitbucket](../providers/bitbucket.md) integration. Pull requests are matched
  against that branch, so an environment following `main` creates previews for pull requests into `main`.
- The integration needs enough access to the repository:
    - GitHub: the GitHub App installation needs write access to `Pull requests`, `Commit statuses`, and `Issues`, and the
      `Pull request` and `Issue comment` events. With Wodby CI, it also needs the `Push` event. GitHub asks the
      installation owner to approve these when they are missing. See
      [GitHub](../providers/github.md#preview-environments).
    - GitLab: the `Maintainer` role on the project and, for an access token, the `api` scope. See
      [GitLab](../providers/gitlab.md#preview-environments).
    - Bitbucket: the `Admin` permission on the repository. See
      [Bitbucket](../providers/bitbucket.md#preview-environments).
- The base environment must not use [Application Access](access.md). Environments with `Public` or `Basic Auth`
  access are supported.
- Database services of the base environment must run as containers in the environment. Environments that use an
  existing database server are not supported yet.
- The cluster of the base environment must allow the environment type chosen for previews. See
  [Environment types](environment-types.md).

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
| `Base environment` | The environment whose configuration is copied into every preview and whose services provide seed data. Only standard environments of the app are offered. Choosing a production environment shows a warning: previews copy its variables and secrets, and seeded services get its data. |
| `Environment type` | The [environment type](environment-types.md) of created previews. `feature` is the default; `prod` is not allowed. |
| `Run cron jobs` | Whether previews run the base environment's cron jobs. Disabled by default: cron jobs are copied but turned off, so previews don't send duplicate emails or run scheduled tasks twice. You can still turn on a single cron job in a preview. |
| `Draft pull requests` | Whether draft pull requests get previews. Disabled by default; a preview is created when the draft is marked ready for review. |
| `Concurrent previews` | The maximum number of preview environments the app keeps at the same time, up to 50. Pull requests beyond the limit are skipped until a preview is deleted. The default is 5. |
| `Idle expiry (days)` | Deletes a preview whose pull request had no activity for this many days. The default is 7 and the maximum is 90; `0` disables idle expiry. |
| `Basic Auth` | Protects every preview with basic auth. Enabled by default. All previews of the app share one generated password. See [Basic auth](#basic-auth). |
| `Seed data` | Base environment services that support both imports and backups. Select a service to restore a fresh backup of it into every new preview, and choose the import and backup when the service offers more than one. |

Seeding a service requires a [backup preset](backups.md) for the chosen backup in the base environment. Services
without one are listed with a `No backup preset` tag and cannot be selected until a preset exists; the tag links to the
base environment's presets.

If seeding a selected service is not possible when a preview is created, the preview is still created and that service
starts without data. This happens when the preset was deleted, or the service was removed, disabled, or not in `OK`
status in the base environment. Wodby reports it on the pull request (see [Pull request feedback](#pull-request-feedback)).
Deleting a backup preset that previews seed from finishes with a warning that explains this.

Changes to these settings apply to previews created afterwards, and existing previews keep running until their pull
request closes or they expire. The exception is `Idle expiry (days)`, which also applies to existing previews, so lowering
it can delete previews soon after you save.

## What a preview contains

Each preview is created from the base environment at the moment the pull request is picked up:

- Service configuration is copied: enabled services and versions, settings, environment variables, volume sizes,
  integrations, cron schedules, and service links. Secret values are copied as well, so pull request code can reach the
  same external services as the base environment.
- Every service runs one replica, with autoscaling turned off. CPU and memory requests and limits stay as in the base
  environment.
- Backup presets are not copied, so previews make no scheduled backups. You can still back up a preview manually.
- Cron jobs are turned off unless `Run cron jobs` is enabled.
- The service connected to the pull request repository follows the pull request branch instead of the base branch.
- Container database services get their own database.
- Only the services selected in `Seed data` get data. They are seeded from a fresh backup of the base environment taken
  at creation time. The backup is
  restored during the preview's first deployment, so a large database delays the first successful deployment.
- Custom domains, TLS certificates, and Application Access are not copied. The preview is reached through its
  generated technical domain.
- Service basic auth entries and exemptions are copied with their passwords. With `Basic Auth` enabled, the shared
  preview password replaces the base environment's environment-wide entry. With it disabled, that entry is copied as it
  is. Entries and exemptions for a single domain are not copied.

The environment machine name is `pr-<number>`, the title shows the pull request number and title, and the technical
domain follows the usual `*.pr-<number>.[app-name].[org-name].wodby.app` pattern. Previews count toward app-service
plan usage like any other environment while they exist.

## Lifecycle

| Event | Result |
| --- | --- |
| Pull request opened, reopened, or marked ready for review | A preview is created when the pull request targets the base environment's branch and no preview exists yet. A push to a pull request without a preview also creates one, for example after enabling previews for an open pull request. |
| Push to the pull request branch | With Wodby CI, the preview is rebuilt and redeployed with the new commit, and a push that arrives while a deployment is running is built after that deployment finishes. With a third-party CI system, your pipeline starts the build. |
| Pull request closed or merged | The preview is deleted. If deletion cannot start, for example while a build is running, Wodby retries it automatically. |
| No activity for the idle expiry period | The preview is deleted. |
| Pull request from a fork | No preview is created. Forks could run untrusted code with the app's configuration. |
| Draft pull request | No preview is created unless `Draft pull requests` is enabled. |
| Concurrent preview limit reached | The pull request is skipped and gets a failed `wodby/preview` status. It gets a preview on its next push once a preview has been deleted. |

Wodby also checks open pull requests every 15 minutes, in case it missed a notification from your Git provider. A
preview whose pull request was closed or merged is deleted. An open pull request that should have a preview gets one, for
example right after you enable previews for an app with open pull requests. A pull request whose latest commit already has a
`wodby/preview` status is left alone, so a preview you deleted is not recreated until the next push.

Automatic preview deletion is not blocked by the organization's [termination protection](../org.md#termination-protection).
You can also delete a preview manually from the app's environments list; the next push to the pull request creates a
new one.

## Basic auth

With `Basic Auth` enabled, every preview asks visitors for a username and password. All previews of the app share one
password, which Wodby generates when previews are enabled, so reviewers learn it once. The username is `wodby`.

On `Apps > [App] > Settings > Preview environments` you can:

- reveal the password. This requires [secret reveal permission](../access-control.md#secret-reveal-permissions) in the
  environment type used for previews, and a recent
  [secret reveal confirmation](../user/security.md#secret-reveal-confirmation). Each reveal is recorded as a task.
- regenerate the password. Every existing preview switches to the new password, and reviewers need the new one.

These actions are available while `Basic Auth` is enabled. Services with their own basic auth entry keep their own
password in previews. Turning `Basic Auth` on or off applies to previews created afterwards; existing previews keep their
current protection until they are deleted.

## Creating a preview manually

To create a preview for an open pull request yourself, open `Apps > [App] > Environments` and click `New PR preview`,
or choose it below `New environment` in the environment menu. Select the pull request and click `Create`. You need
permission to create environments of the app.

The list shows the open pull requests into the base environment's branch. Pull requests that cannot get a preview are
shown disabled with the reason, such as a pull request from a fork or one that already has a preview. Draft pull
requests can be selected even when `Draft pull requests` is disabled. The concurrent preview limit still applies.

If previews are not configured for the app yet, the page links to the app's preview environment settings instead.

## Pull request feedback

Wodby reports each preview deployment to the pull request as a `wodby/preview` commit status on the commit it built:
in progress while the environment is being created, then successful or failed with a link to the preview.

Wodby also keeps one comment on the pull request and edits it as the preview changes: when it is being created, when
it is ready (with the preview URL), when a deployment fails, when a preview cannot be created and why, when services
start without seed data, and when the preview is deleted. If you delete the comment, Wodby posts a new one on the next
change. When a preview is password-protected, the comment links to the preview in the dashboard and never contains the
password.

A deployment that did not build the pull request commit, such as a configuration-only redeploy, does not change the
status.

When Wodby cannot create a preview for a pull request, it sets the `wodby/preview` status to failed with the
reason, for example that the base environment is not in `OK` status or that the concurrent preview limit is reached.
The next push to the pull request tries again.

When a preview is created but some selected services could not be seeded, Wodby also sets a `wodby/preview-data`
status to failed that names the service and the reason, or the number of affected services. The preview itself
works; those services start without data. Fix the cause, such as adding the missing backup preset, then comment
`/wodby reseed` on the pull request to create the preview again with data.

## Pull request commands

Comment on the pull request with one of these commands on its own line:

| Command | Result |
| --- | --- |
| `/wodby preview` | Creates a preview for the pull request, following the same rules as [creating a preview manually](#creating-a-preview-manually). |
| `/wodby reseed` | Deletes the preview and creates it again from the base environment, with fresh seed data. The preview's address can change, and the Wodby comment shows the new one. If creating the new preview fails after the old one started deleting, the pull request is left without a preview, and the Wodby comment says how to ask for a new one. |

Who can run commands depends on the provider:

| Provider | Who can run commands |
| --- | --- |
| GitHub | People with write, maintain, or admin access to the repository. |
| GitLab | Project members with the `Developer` role or higher. |
| Bitbucket | People with write or admin access to the repository. The integration's Bitbucket account must have the `Admin` permission on the repository, because Bitbucket shows permissions only to admins. Without it, every command is refused. |

On GitHub and GitLab, Wodby reacts with 👍 when it accepts a command and with 😕 when it refuses one. If someone with
access gives a command that cannot run, the Wodby comment explains why. Bitbucket has no reactions, so every refusal is
explained in the Wodby comment.

`/wodby reseed` is refused while the preview cannot be deleted, for example while a build is running. Commands are
ignored for apps without preview environments.

## Using previews from AI agents

Agents connected through the [Wodby MCP server](../dev/mcp.md) can read and change an app's preview settings,
list pull requests that can get a preview, and create one, with the
[preview tools](../dev/mcp/tools.md). Changing settings and creating a preview require your confirmation.

## Finding previews in the dashboard

Preview environments appear in `Apps > [App] > Environments` with a `PR #<number>` tag and can be opened like any other
environment. Their creation, deployments, and deletion are listed under the app's `Tasks` tab, where the creation task is
titled with the pull request number.

If a pull request does not get a preview, check the Wodby comment or the `wodby/preview` status on the pull request
for the reason. Also check
that previews are enabled for the app, that the pull request targets the branch the base environment follows, and that
it is not a draft or from a fork.

## Related pages

- [App environments](environments.md)
- [Applications overview](index.md)
- [Backups](backups.md)
- [Imports](imports.md)
- [GitHub](../providers/github.md)
- [GitLab](../providers/gitlab.md)
- [Bitbucket](../providers/bitbucket.md)
