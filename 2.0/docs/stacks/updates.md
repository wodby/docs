# Stack updates

Stacks are versioned. Stack updates and configuration edits create or update an unpublished draft revision first. The
currently published revision remains active for running app instances until you publish the draft.

Publishing the draft creates a new stack revision, but it does not automatically change running app instances. After the
revision is published, each app instance can be upgraded separately from its current revision to the latest revision.

There are three common update paths.

## Update stack service revisions

Use this for stacks managed in the dashboard.

Open `Stacks`, select the stack, and stay on the `Overview` tab. When an owned stack is marked `Outdated`, the
`Stack update` card appears with an `Update services to latest version` button.

When a service used by the stack has a newer service revision, Wodby can update the stack services to point to the
latest service revisions in the draft revision.

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

This workflow does not update Git-backed stacks. For Git-backed stacks, the `Stack update` card shows a warning and the
`Update stack` button is disabled. Use `Edit` > `Update` for those stacks instead.

## Update from Git

Use this for stacks imported from a Git repository.

Open `Stacks`, select the stack, and go to `Edit`. Git-backed stacks show an `Edit stack` form with the current
repository, ref type, and Git ref. Select the Git tag or branch to import and click `Update`.

Wodby imports the stack definition from the selected Git ref, finds the same stack by name, and creates or updates the
draft revision from the updated `stack.yml`.

Use this workflow when the stack manifest itself changed in Git, for example when services were added or removed,
stack-level defaults changed, or stack service configuration changed.

The update form is available only on the latest stack revision. Older stack revisions can be viewed, but they cannot be
updated from Git.

## Sync with origin

A copied catalog stack keeps a reference to the origin stack revision it was copied from. Syncing with origin creates or
updates your draft revision from the latest origin revision.

Open `Stacks`, select the copied stack, and stay on the `Overview` tab. If the stack has an origin, the `SYNC` card
appears with a `Sync with origin` button.

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

The sync form also has advanced deletion options for cases where you want the local stack to become closer to the
origin:

| Dashboard option | Effect |
| --- | --- |
| Keep only origin stack env vars | Delete stack-level environment variables that do not exist in the origin. |
| Keep only origin stack tokens | Delete stack-level tokens that do not exist in the origin. |
| Keep only origin stack-level annotations | Delete stack-level annotations that do not exist in the origin. |
| Keep only origin stack services | Delete stack services that do not exist in the origin. |
| Keep only origin stack services configuration | For services that exist in both stacks, delete service-level configuration entries that do not exist in the origin. |

Stack service configuration includes service-level Helm values, environment variables, volumes, tokens, settings,
options, resource overrides, cron schedules, configs, and links.

The dashboard sync form does not expose a deletion option for stack-level Helm values.

Sync with origin is the right workflow when you copied a catalog stack and want to pull in catalog-side manifest
changes such as newly introduced services, newly introduced stack service defaults, or removed services. Use the
deletion options only when you are comfortable removing local stack customizations that are no longer present in the
origin.

## Publish or discard a draft

After any stack edit or update workflow creates a draft, the stack shows an unpublished draft notice.

Use `Publish draft` when you are ready to release the draft as a real stack revision. Publishing is the point where app
instances using older stack revisions can become outdated.

Use `Discard` to delete the draft and abandon the unpublished changes. After discard, the stack returns to its current
published revision and app instances are unaffected.

## App instance upgrades

After a draft is published as a new stack revision, app instances still run their current stack revision until you
upgrade them.

Open `Apps`, select the app, select an app instance, and go to the `Stack` tab. See
[Application stack](../apps/stack.md#upgrade) for the app instance upgrade workflow and the available upgrade settings.
