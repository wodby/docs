---
description: Update a Wodby service from Git or a manifest, turn on auto-update, see how revisions reach stacks, and archive services you no longer need.
---

# Service updates

Services are versioned. Updating a service creates a new service revision. Stacks that use the service decide when to
move to that new revision, either through a manual stack update or stack service revision auto-update.

## Update from Git

Use this for services imported from a Git repository.

Open `Services`, select the service, and go to `Operations`. The `Manual update from Git` card shows the current
repository and Git ref. Select the Git tag or branch to import and click `Update`.

Wodby imports the service definition from the selected Git ref and creates a new service revision from the updated
service template.

Use this workflow when the service template changed in Git, for example when workloads, images, Helm values, settings,
configs, links, integrations, volumes, cron schedules, or other manifest sections changed.

The update form is available only on the latest service revision. Older service revisions can be viewed, but they
cannot be updated from Git.

## Update from a local manifest

Use this for services created from a manifest rather than imported from Git.

Open `Services`, select the service, and go to `Edit`. The `Manual update from manifest` card shows the current
manifest. Edit it, or select `Read manifest from file` to load an updated `service.yml`. If the manifest references
local files such as configs or Dockerfiles, add them under `Additional files` with the same paths the manifest uses.
Set the `Version` of the new revision and click `Update`.

Wodby creates a new service revision from the manifest. Keep in mind:

- The manifest `name` and `type` cannot change.
- If the manifest matches the current revision, no new revision is created.
- If you clear `Version`, the new revision keeps the current version.
- The update form is available only on the latest service revision.

## Updates to inherited services

An inherited service can select its base service revision with an exact `fromVersion`, a compatible
`fromVersionConstraint`, or both:

- `fromVersion` pins the inherited service to that exact base service version.
- `fromVersionConstraint` without `fromVersion` selects the greatest compatible semantic version from the base
  service's available revision history whenever the inherited service is imported or updated.
- When both are set, `fromVersion` selects the base version and must satisfy `fromVersionConstraint`.

When an exact pin selects an older base revision, the update still succeeds and its task log warns which base revision
was used and which revision is current. The service page also shows this difference. If the exact `fromVersion` is
absent from the available base service revision history, the update fails instead of silently substituting another
version.

Compatible base service revisions can also update an inherited service automatically. This applies only when all of
the following are true:

- `Base service auto update` is enabled for the inherited service.
- The inherited service is Git-backed and tracks a branch.
- Its source template includes `fromVersionConstraint` without an exact `fromVersion` pin.
- The new base service version satisfies the constraint.

After a successful compatible base service revision is published, Wodby imports the inherited service from its tracked
branch and creates a new inherited service revision. The setting is independent of `Auto update from Git`, so the
inherited service does not need a new commit. The base service itself does not have to be Git-backed.

Tag-backed, commit-pinned, non-Git-backed, and non-inherited services cannot enable base service auto-update. An exact
`fromVersion` also remains pinned. Update the inherited service's source or manifest explicitly when it should move to
another base revision.

In the dashboard, the service page shows the base service version constraint. For eligible branch-backed services,
enable `Operations > Base service auto update`. Organization administrators receive the existing automatic service
update success and failure email notifications for these updates, subject to their notification preferences. Stacks
still control when they move to the newly created inherited service revision.

## Delete a Git-backed service

Open `Services`, select the service, and go to `Edit`. Git-backed services show the delete action on the `Edit` tab,
not on the `Operations` tab. The delete action is available only on the latest service revision.

A base service cannot be deleted while inherited service revisions reference its revision history.

## Archive a service

Archive a service you no longer need but cannot delete because earlier stack revisions still use it. The stack
revisions and app environments that already use the service keep working, including deployments and stack upgrades.

An archived service:

- is listed after the services in use on the `Services` page and marked `Archived`
- cannot be added to a stack, used by a new or copied stack, or used as the base service of another service
- is not updated from Git, manually or automatically, and its update settings cannot be changed
- is not scanned for vulnerabilities

To archive a service, open `Services`, select the service, go to `Edit`, and click `Archive service`. To use it again,
click `Unarchive service` on the same tab. Both actions are available only on the latest service revision.

You cannot archive a service while:

- the current or draft revision of a stack uses it. Remove or replace the service in those stacks first.
- a service that is not archived inherits from it. Archive or delete that service first.

The error message lists the stacks or services to change. You can still delete an archived service once no stack
revision uses it.

### Services removed from Git

A Git repository can hold several services. When you remove one of them from the repository, Wodby keeps the service
at its last revision and archives it the next time the service is updated from Git, if the rules above allow it.
Otherwise the update task ends with a warning that lists what still uses the service. Wodby does not delete services
removed from Git.

If the service returns to the repository and the service updates from Git automatically, the next automatic update
unarchives it and imports the new revision. Otherwise, unarchive the service and update it from Git. A service you
archived yourself stays archived until you unarchive it.

## Auto-update from Git

Git-backed services can be updated automatically when a supported Git provider sends a push event for the service
source. Auto-update works like manual `Update from Git`, but starts on the push event instead of a dashboard action.

The auto-update settings decide which push events are allowed:

- Branch updates run only when the pushed branch matches the service's tracked Git ref.
- Tag updates run only when the service currently tracks a valid semantic-version tag and the pushed tag is a newer
  semantic version.
- Tag updates can be limited to patch, minor, or major version changes.
- Commit-pinned services are not auto-updated.

When auto-update is enabled, choose either branch updates or semantic-version tag updates. Semantic-version tag updates
can be enabled only when the service currently tracks a valid semantic-version Git tag.

Service auto-update creates a new service revision from Git. Stacks that use the service still control when they move to
the new service revision. Stacks can be updated manually, and stacks with stack service revision auto-update enabled can
move to newer allowed service revisions automatically.

Auto-update settings are stored on the connected Git repository. If multiple services or stacks use the same repository,
changing the settings from one resource changes auto-update behavior for the other resources that share it.
