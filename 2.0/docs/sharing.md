# Sharing

Projects isolate resources by default. When you need to reuse a resource in another project, you share it to that project explicitly.

This is the supported way to work across project boundaries.

## What sharing does

Sharing makes a resource visible in one or more additional projects without moving ownership out of the original project.

This is useful when, for example:

- several projects should use the same Kubernetes cluster
- one project should consume a database owned by another project
- a shared provider or integration should be available to multiple teams

## How sharing is configured

For supported resource types, open the resource and go to its `Sharing` screen.

Each target project has two controls:

- `Access` makes the resource visible in that project
- `Writable` removes the read-only restriction for that project

If you enable `Writable`, Wodby automatically enables `Access`. If you disable `Access`, the share is removed.

## Current dashboard support

| Resource | Sharing in dashboard | Notes |
| --- | --- | --- |
| Kubernetes clusters | Yes | Can be shared per project as read-only or writable |
| Databases | Yes | Can be shared per project as read-only or writable |
| Integrations | Yes | Can be shared per project as read-only or writable |
| Services | Yes | Sharing is available only on the latest revision |
| Stacks | Yes | Sharing is available only on the latest revision |
| Providers | Yes | Sharing is available only for org-owned providers |
| Apps | No dedicated sharing screen | Apps are project-scoped, but the dashboard does not currently expose a dedicated app sharing tab |

## Read-only vs writable

Read-only sharing is strict.

- The resource appears in the target project.
- Users in the target project can select or reference it where the workflow allows.
- They cannot modify the shared resource itself.
- This read-only restriction still applies even if the user is a project admin in the target project.

Writable sharing removes that restriction for the target project.

## Where shared resources appear

Shared resources appear in the target project's `Resources` view. That page also shows whether the share is read-only.

Once visible in the target project, the resource can be used by project-aware workflows there, such as app deployment or service configuration, subject to normal compatibility rules.

## Practical rule

If a resource from Project A is missing while you work in Project B, the first thing to check is whether that resource has been shared to Project B.

Without that share, cross-project references are not available.

## Related pages

- [Projects](projects.md)
- [Access control](access-control.md)
