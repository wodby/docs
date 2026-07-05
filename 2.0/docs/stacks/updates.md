# Stack updates

Stacks are versioned. Dashboard-managed stack configuration edits create or update an unpublished draft revision first.
The currently published revision remains active for running app instances until you publish the draft.
Stack service revision updates, Git updates, sync with origin, and automatic stack updates create a new stack revision
directly after the update task succeeds.

Publishing a draft or completing a stack update does not automatically change running app instances. Automatic stack
updates can also auto-upgrade app instances when auto-upgrade is enabled for those instances. After a new revision
exists, each app instance can still be upgraded separately from its current revision to the latest revision.

There are several common update paths.

## Update stack service revisions

Use this when the stack should keep the same stack definition but move included services to newer service revisions.

Open `Stacks`, select the stack, and go to `Operations`. Owned stacks show a `Service update` card with an
`Update services to latest version` button.

When updates are available, the card lists the affected services and shows the current and latest service revision
versions. When every unpinned service already uses the latest available service revision, the card shows an `Up to date`
tag and the update button is disabled.

When a service used by the stack has a newer service revision, Wodby can update the stack services to point to the
latest service revisions in a new stack revision.

This is also the path to refresh service option metadata used for EOL review. If a stack shows an `EOL` flag, update the
stack services to the latest service revisions before checking exact EOL dates or selecting newly available non-EOL
versions.

This update keeps stack service names and valid stack-level configuration. It is intended for service-template changes
inside services that are already part of the stack, such as newer images, Helm changes, added settings, added configs,
added links, new resource defaults, or new cron definitions.

If a stack-level override no longer matches the new service revision, Wodby may remove the invalid override while keeping
the rest of the stack configuration. For example, a config override can be removed if the service no longer defines that
config, a cron override can be removed if it targets a workload that no longer exists, or an integration can be removed if
the linked integration no longer satisfies the service requirements.

When Wodby chooses a safe fallback during the update, the update task can finish with warnings. Open the task logs to
review what changed. Warnings can include removed invalid overrides or derivative stack services created with a fallback
name because the expected name was already taken.

This workflow can be used for dashboard-managed and Git-backed stacks. For Git-backed stacks, it does not fetch the
stack repository or apply `stack.yml` changes. Use `Update from Git` when the stack manifest itself changed, or when you
want to change a pinned/versioned service reference from Git.

## Auto-update stack service revisions

Use this for stacks that should follow newer service revisions without a manual stack update step.

When auto-update is enabled for stack service revisions, Wodby can create a new stack revision after a service used by
the stack gets a newer revision. This uses the same reconciliation as the manual `Update services to latest version`
workflow, including task logs and warnings for removed invalid overrides.

For custom stacks, auto-update is disabled by default. Git-backed stacks can use this setting for service revision
updates; Wodby updates stack service rows in a new stack revision without fetching the stack repository.

In the dashboard, open `Stacks`, select the stack, and go to `Operations`. Service revision automation is configured in
the `Services auto update` card. For Git-backed stacks, this card is shown separately from `Auto update from git`, which
controls Git imports.

Wodby catalog stacks added from the catalog enable this setting by default unless you turn off `Services auto update`
in the `Add stack` form. Their default policy updates stateless services only, uses semantic-version mode, allows patch
and minor updates, and disables major updates.

Pinned stack services are skipped by manual and automatic service revision updates. They do not make the stack
`Outdated`. Pin a stack service when it should stay on its current service revision until you explicitly unpin it or
update the stack from Git with a different service reference.

Disabled stack services are still considered by manual and automatic service revision updates. If a disabled service
should stay on its current service revision, pin it.

The stack auto-update policy controls which service revision changes are allowed. Choose the service update scope and
one version mode: semantic-version updates, non-semver updates, or revision updates.

| Option | Effect |
| --- | --- |
| Update stateless only | Update only services whose target manifests have no database, StatefulSet workloads, or owned persistent volumes. |
| Update all services | Allow stateful and stateless services. Use this only when the stack can accept automatic stateful-service changes. |
| Semantic-version updates | Update only when the current and target service versions are valid semantic versions and the target is newer. |
| Non-semver updates | Update only when the target service version is non-empty, non-semver, and different from the current service version. |
| Revision updates | Update whenever the target service revision changed, even when the service version string stayed the same. |
| Allow patch, minor, or major versions | In semantic-version mode, limit updates by version segment. |

By default, the saved policy allows patch and minor semantic-version updates for stateless services. It does not allow
major version updates or non-semver version changes unless you enable those options. When you enable service revision
auto-update for a Git-backed stack in the dashboard, `Update stateless only` is selected by default; review the scope
before saving if the stack can accept automatic stateful-service changes.

For the `Update stateless only` scope, a service that mounts storage from another service is not treated as the storage
owner. Volumes that borrow storage with `from` or delegate storage to a linked storage service with `shared` and `link`
can still be updated under the stateless-only policy.

Use revision mode for services imported from a branch, such as `main`, when each service revision may keep the same
service version string.

## Update from Git

Use this for stacks imported from a Git repository.

Open `Stacks`, select the stack, and go to `Operations`. Git-backed stacks show an `Update from Git` card with the
current repository, ref type, and Git ref. Select the Git tag or branch to import and click `Update`.

Wodby imports the stack definition from the selected Git ref, finds the same stack by name, and creates a new stack
revision from the updated `stack.yml`.

Use this workflow when the stack manifest itself changed in Git, for example when services were added or removed,
stack-level defaults changed, or stack service configuration changed.

The update form is available only on the latest stack revision. Older stack revisions can be viewed, but they cannot be
updated from Git.

## Delete a Git-backed stack

Open `Stacks`, select the stack, and go to `Edit`. Git-backed stacks show the delete action on the `Edit` tab, not on
the `Operations` tab. The delete action is available only on the latest stack revision.

## Auto-update from Git

Git-backed stacks can be updated automatically when a supported Git provider sends a push event for the stack source.
Auto-update uses the same import logic as manual `Update from Git`, but it is started by the webhook instead of a
dashboard action.

In the dashboard, Git auto-update settings for stacks are shown in `Operations > Auto update from git`. Keep them
separate from `Services auto update`: Git auto-update imports the stack manifest from Git, while service revision
auto-update keeps the current stack revision definition and updates eligible stack service revision references.

The auto-update settings decide which push events are allowed:

- Branch updates run only when the pushed branch matches the stack's tracked Git ref.
- Tag updates run only when the stack currently tracks a valid semantic-version tag and the pushed tag is a newer
  semantic version.
- Tag updates can be limited to patch, minor, or major version changes.
- Commit-pinned stacks are not auto-updated.

When auto-update is enabled, choose either branch updates or semantic-version tag updates. Semantic-version tag updates
can be enabled only when the stack currently tracks a valid semantic-version Git tag.

New Git-backed catalog stacks default to auto-update enabled. Branch-based stacks follow the tracked branch. Tag-based
stacks follow newer semantic-version tags, with patch and minor updates allowed by default and major updates disabled.
Custom Git-backed stacks can use the same settings when they should follow their source repository automatically.

Auto-update is skipped while a stack is already updating, while another stack update task is active, or while the stack
has an unpublished draft. Resolve the draft first, then run the update again or wait for the next matching push event.

## Sync with origin

A copied catalog stack keeps a reference to the origin stack revision it was copied from. Syncing with origin creates a
new stack revision from the latest origin revision.

Open `Stacks`, select the copied stack, and go to `Operations`. If the stack has an origin, the `Sync with origin stack`
card appears with a `Sync with origin` button.

Sync is conservative by default:

- missing origin stack tokens, environment variables, Helm values, annotations, stack services, and stack service
  configuration are added to your stack
- existing local values with the same names are kept, so customizations are not overwritten just because the origin
  changed its default
- if the origin introduces a main HTTP service and your stack already has another main service, Wodby clears the old
  main flag when needed to keep only one main service
- if the stack ends up without a main HTTP service, Wodby picks the first HTTP-capable stack service

If the origin changes an existing value under the same name, sync keeps your local value. Review and update those values
manually when you want to adopt the changed origin default.

The sync form also has options for cases where you want the local stack to become closer to the origin:

| Dashboard option | Effect |
| --- | --- |
| Origin Helm values only | Delete stack-level Helm values that do not exist in the origin. |
| Origin env vars only | Delete stack-level environment variables that do not exist in the origin. |
| Origin tokens only | Delete stack-level tokens that do not exist in the origin. |
| Origin annotations only | Delete stack-level annotations that do not exist in the origin. |
| Origin services only | Delete stack services that do not exist in the origin. |
| Origin service config only | For services that exist in both stacks, delete service-level configuration entries that do not exist in the origin. |

Stack service configuration includes service-level Helm values, environment variables, volumes, tokens, settings,
options, resource overrides, cron schedules, configs, and links.

Sync with origin is the right workflow when you copied a catalog stack and want to pull in catalog-side manifest
changes such as newly introduced services, newly introduced stack service defaults, or removed services. Use the
deletion options only when you are comfortable removing local stack customizations that are no longer present in the
origin.

## Auto-sync with origin

Use this for copied catalog stacks that should follow their origin stack automatically.

When origin auto-sync is enabled, Wodby can create a new stack revision after the origin stack publishes a new
revision. The first check is revision-based: if your stack still points to an older origin revision, it becomes a
candidate for sync.

When you add a Wodby catalog stack, the `Add stack` form shows `Auto sync with origin` enabled by default. Turning that
switch off creates the stack with origin auto-sync disabled. When enabled by default, origin auto-sync uses
semantic-version mode with patch and minor updates allowed, major updates disabled, and no deletion options. Origin
auto-sync is available only for stacks that have an origin stack revision and are not Git-backed.

In the dashboard, origin auto-sync settings are shown in the `Auto sync with origin stack` card next to
`Services auto update`.

The origin version policy controls which origin revisions are allowed:

| Option | Effect |
| --- | --- |
| Semantic-version updates | Sync only when the previously tracked origin version and target origin version are valid semantic versions and the target is newer. |
| Non-semver updates | Sync only when the target origin version is non-empty, non-semver, and different from the previously tracked origin version. |
| Allow patch, minor, or major versions | In semantic-version mode, limit updates by version segment. |

The default origin auto-sync version policy uses semantic-version mode with patch and minor updates allowed and major
updates disabled. EOL status does not control origin auto-sync.

If the previously tracked origin version is not semantic-version compatible and the target origin version is semantic
version compatible, origin auto-sync skips the change in both modes. Semantic-version mode requires both versions to be
valid semantic versions, and non-semver mode accepts only non-semver target versions.

Sync behavior is conservative by default. Without deletion options, missing origin objects are added, and local objects
that are not present in the origin are preserved.

You can also configure origin auto-sync to prune local objects that no longer exist in the origin. The available
auto-sync deletion options match manual sync:

| Auto-sync option | Effect |
| --- | --- |
| Keep only origin stack env vars | Delete stack-level environment variables that do not exist in the origin. |
| Keep only origin stack Helm values | Delete stack-level Helm values that do not exist in the origin. |
| Keep only origin stack tokens | Delete stack-level tokens that do not exist in the origin. |
| Keep only origin stack-level annotations | Delete stack-level annotations that do not exist in the origin. |
| Keep only origin stack services | Delete stack services that do not exist in the origin. |
| Keep only origin stack services configuration | For services that exist in both stacks, delete service-level configuration entries that do not exist in the origin. |

Use deletion options only when the copied stack should closely mirror the catalog origin. Leave them disabled when the
stack has local customizations that should survive catalog changes.

## Publish or discard a draft

After any stack configuration edit creates a draft, the stack shows an unpublished draft notice.

Use `Publish draft` when you are ready to release the draft as a real stack revision. Publishing is the point where app
instances using older stack revisions can become outdated.

Use `Discard` to delete the draft and abandon the unpublished changes. After discard, the stack returns to its current
published revision and app instances are unaffected.

## App instance upgrades

After a draft is published as a new stack revision, app instances still run their current stack revision until you
upgrade them.

Open `Apps`, select the app, select an app instance, and go to `Stack > Operations`. See
[Application stack](../apps/stack.md#upgrade) for the app instance upgrade workflow and the available upgrade settings.
