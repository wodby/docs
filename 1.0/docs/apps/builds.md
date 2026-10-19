# Builds

Open **Instance > Builds** to review CI build history, inspect service images, deploy a previous build, or configure image cleanup. The tab has **List** and **Settings** views. Use [third-party CI](../cicd/third-party.md) to create and deploy new builds.

## Build history

The **List** view shows:

| Column | Details |
| --- | --- |
| Build | Build number, with a **Current** label for the instance's current build |
| Provider | CI provider, or **Custom CI** when none is recorded |
| Source | Repository, branch, and tag when recorded |
| Commit | Abbreviated commit identifier |
| Images | Image count and a summary of their lifecycle status |
| Deployed | The build's original deployment time |

Use the page controls to browse older builds. If history cannot be loaded, click **Retry**. An empty history displays **No builds found**.

## Build details

Click a build number to see its original deployment time, CI provider and build URL, repository, branch or tag, commit, and stack version when available. The **Built images** table lists each service's image reference and status.

Image statuses include:

- **Active**: images used by a current deployment.
- **Retained**: managed images retained for a historical build.
- **Queued for deletion**: images have been voided and are awaiting registry cleanup.
- **Deleted from registry**: managed images have been removed.
- **External registry**: images are stored outside Wodby's registry.

The list summarizes voided images as **Voided** or **Partially voided** and shows **No images** when none are recorded. Review the individual image statuses and deployment warnings before reusing a build.

## Automatically clean unused build images

CI build images remain in the registry after a newer build is deployed so you
can [deploy a previous build](#deploy-a-previous-build).

To set the retention period in [Organization settings](../org/settings.md), open
`Organization > Settings > Builds` and configure **Auto-void images of unused
builds for all apps older than**. When you save a new organization default,
Wodby updates existing app instances only when their current setting matches
the organization's previous default. Instance settings with a different value
are treated as overrides and remain unchanged. New app instances inherit the
current organization default.

To override the organization default for one app instance, open
`Instance > Builds > Settings`, configure **Auto-void images of unused builds older than**,
and click **Save**. Both settings offer periods of 1 month, 3 months, 6 months, and 1 year. The initial
default is **Never**.

Retention is measured from the build's original creation date. When retention
is enabled or shortened, existing unused builds that are already older than the
selected period become eligible immediately. Cleanup runs in the background,
so an eligible image may remain for a short time after reaching that age.

Wodby never automatically cleans images that are referenced by any instance's
current build. If a previous build becomes current again before cleanup, its
images remain protected regardless of the build's age. Selecting **Never**
disables automatic cleanup; enabling it again evaluates unused builds from
their original creation dates.

Cleanup removes managed image tags from Wodby's registry but preserves the
build history. A historical build whose required images have been removed
cannot be deployed again. Images stored in an external registry are not
deleted by this setting.

## Deploy a previous build

For an application instance that uses CI deployment, open `Instance > Builds`,
select a non-current build, and click **Deploy this build**. Wodby shows a
confirmation with the current and selected build numbers, the original build
date and source, the stack version change, the recorded service images, and any
eligibility warnings.

The operation makes the selected build's saved service images current. If the
build used an older revision of the same stack, that exact stack revision also
becomes active. The newer revision remains pending, and the instance is marked
as requiring a rebuild so you can return to the newer stack with a new CI
build. Deploying the previous build does not modify its original build record
or timestamp.

!!! warning "A previous build is not a complete instance restore"
    The database and persistent files are not rolled back. Current instance
    settings still control whether post-deployment scripts run, and those
    scripts can modify persistent data. Wodby does not automatically restore
    the previous deployment if the task fails or only partially completes.

Before confirming:

1. Verify that recent database and file backups are available and restorable.
2. Check that the selected application code and stack are compatible with the
   current database schema and persistent data.
3. Review every service image, its registry status, and all warnings in the
   confirmation.
4. Check the current post-deployment script setting and make sure those scripts
   are safe to run with the selected build.
5. Plan for service restarts or short downtime, then monitor the deployment
   task logs and application health after confirmation.

Deployment is blocked when the stack revision no longer exists, belongs to a
different logical stack, or cannot be prepared; when a required image is
missing, voided, or deleted; or when a Drupal stack migration is pending.
Images stored in an external registry cannot be verified by Wodby, so their
availability is shown as a warning instead.

## Void unused build images

Open `Instance > Builds > List`, select an unused historical build, and click
**Void build images**. Review the confirmation and click **Void images** to queue
its managed image tags for deletion without waiting for the retention period.
This cannot be undone. Wodby never offers this action for a build that is current
on an instance. The build record remains in history, but voided images cannot
be used to deploy it again, even while registry cleanup is pending. Registry deletion, usage
measurement, and billing reconciliation run asynchronously, so the displayed
storage total does not change immediately.

See [Container registry storage](../billing.md#container-registry-storage) for how cleanup affects billing.
