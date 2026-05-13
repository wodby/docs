# Stack updates

Stacks are versioned. Any stack update creates a new stack revision, but it does not automatically change running app
instances. After the stack revision is created, each app instance can be upgraded separately from its current revision
to the latest revision.

There are three common update paths.

## Update stack service revisions

Use this for stacks managed in the dashboard.

When a service used by the stack has a newer service revision, Wodby can update the stack services to point to the
latest service revisions and create a new stack revision.

This update keeps the stack service names and stack-level configuration. It is intended for service-template changes
inside services that are already part of the stack, such as newer images, Helm changes, added settings, added configs,
added links, new resource defaults, or new cron definitions.

This workflow does not update Git-backed stacks. Git-backed stacks are updated from Git instead.

## Update from Git

Use this for stacks imported from a Git repository.

Wodby imports the stack definition from the selected Git ref, finds the same stack by name, and creates a new stack
revision from the updated `stack.yml`.

Use this workflow when the stack manifest itself changed in Git, for example when services were added or removed,
stack-level defaults changed, or stack service configuration changed.

## Sync with origin

A copied catalog stack keeps a reference to the origin stack revision it was copied from. Syncing with origin creates a
new revision of your stack from the latest origin revision.

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

The sync form also exposes deletion options for cases where you want the local stack to become closer to the origin:

| Option | Effect |
| --- | --- |
| Delete stack Helm values | Delete stack-level Helm values that do not exist in the origin. |
| Delete stack env vars | Delete stack-level environment variables that do not exist in the origin. |
| Delete stack tokens | Delete stack-level tokens that do not exist in the origin. |
| Delete stack services | Delete stack services that do not exist in the origin. |
| Delete stack service configuration | For services that exist in both stacks, delete service-level configuration entries that do not exist in the origin. |

Stack service configuration includes service-level Helm values, environment variables, volumes, tokens, settings,
options, resource overrides, cron schedules, configs, and links.

Sync with origin is the right workflow when you copied a catalog stack and want to pull in catalog-side manifest
changes such as newly introduced services, newly introduced stack service defaults, or removed services. Use the
deletion options only when you are comfortable removing local stack customizations that are no longer present in the
origin.

## App instance upgrades

After any stack update creates a new stack revision, app instances still run their current stack revision until you
upgrade them.

See [Application stack](../apps/stack.md#upgrade) for the app instance upgrade workflow and the available upgrade
settings.
