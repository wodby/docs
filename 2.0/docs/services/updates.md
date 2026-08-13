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

## Updates to inherited services

An inherited service uses the base service revision selected by `fromVersion`. Wodby resolves that exact version from
the base service's revision history, so the inherited service can remain on an older base revision after a newer one is
published.

When an update uses an older base revision, the update still succeeds and its task log warns which base revision was
used and which revision is current. The service page also shows this difference. Wodby does not move the inherited
service automatically unless its template includes a compatible `fromVersionConstraint` and the update source supports
compatible base revision updates.

If the exact `fromVersion` is absent from the available base service revision history, the update fails instead of
silently substituting another version.

## Delete a Git-backed service

Open `Services`, select the service, and go to `Edit`. Git-backed services show the delete action on the `Edit` tab,
not on the `Operations` tab. The delete action is available only on the latest service revision.

A base service cannot be deleted while inherited service revisions reference its revision history.

## Auto-update from Git

Git-backed services can be updated automatically when a supported Git provider sends a push event for the service
source. Auto-update uses the same import logic as manual `Update from Git`, but it is started by the webhook instead of
a dashboard action.

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
