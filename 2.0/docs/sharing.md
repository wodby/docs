# Sharing

Projects isolate resources by default. Sharing is how a resource becomes visible or usable outside its owner scope.

The project-sharing controls on this page apply within one Wodby organization. Eligible OAuth integrations have an
additional owner-approved flow for use across Wodby organizations; see
[Share an OAuth integration with another organization](integrations/organization-sharing.md).

Sharing works together with [access control](access-control.md):

- ownership decides who can directly modify or delete a resource
- sharing decides where the resource can be seen and used, and whether the project-resource link is read-only or write-capable

## What sharing does

Sharing makes a resource available in one or more projects without moving ownership.

This is useful when, for example:

- several projects should deploy apps to the same Kubernetes cluster
- one project should use an integration managed by another project or by the organization
- multiple projects should use the same stack, service, provider, or database
- an organization-owned resource should be available only to selected projects
- an organization-owned cluster, integration, stack, or service should be available to every project
- a platform team should let another project use a shared resource without transferring ownership

## Ownership scopes

A share never changes the resource owner.

| Ownership scope | Who can directly modify/delete the resource | Who can read/use it | Who can change ownership/sharing |
| --- | --- | --- | --- |
| Organization-owned | Organization owners/admins | Organization owners, admins, support users, and users in shared projects. Every organization member when the resource is [available to all projects](#make-a-resource-available-to-all-projects) | Organization owners/admins |
| Project-owned | Users with `Write` or `Admin` access to the owner project, plus organization owners/admins | Users who can access the owner project or any shared project | Organization owners/admins. If the resource remains project-owned, users with owner-scope write access can update sharing or owner project when they also have project `Admin` access to every affected project |

Project shares do not transfer ownership and do not grant project administration rights. Changing any resource to organization ownership requires organization owner/admin access.

## Project access levels

In the dashboard sharing form, project access is controlled with two columns:

| Access level | Meaning |
| --- | --- |
| `Read/Use` | Users in the project can view, select, or reference the resource in supported workflows. |
| `Modify/Delete` | Includes `Read/Use` and marks the project-resource link as write-capable for workflows that check project-resource access. Users still need write-level access in that project. |

Neither access level transfers ownership. A `Modify/Delete` share to a non-owner project does not by itself authorize direct resource update/delete mutations or allow the target project to change the resource owner or sharing settings.

## Read/use access

Read/use access to a shared resource means the resource can be selected or referenced by supported workflows.

Examples:

- a shared cluster can be selected as an app deployment target
- a shared stack can be used to create an app
- a shared integration can be attached to an app service
- a shared service, provider, or database can be used where the resource type is supported

The user still needs write access to the target project or target app they are changing. Sharing the selected resource does not grant permission to create or modify other objects.

## Make a resource available to all projects

An organization-owned Kubernetes cluster, integration, stack, or service can be available to all projects instead of
being shared project by project.

When a resource is available to all projects:

- every project in the organization can use it, including projects created later
- every organization member can see and select it
- every project has `Read/Use` access, and you can still give selected projects `Modify/Delete`
- only organization owners and admins can modify or delete the resource or change its sharing

To change the setting, open the resource, go to `Sharing`, and set `Available to` to `All projects` or
`Selected projects`. You can also select `Available to all projects` when you create, import, or copy a cluster,
integration, stack, or service with the organization as its owner.

Apps, databases, and providers do not have this setting. A project-owned resource does not have it either: change its
owner to the organization first.

Switching back to `Selected projects` is rejected while a project without its own share still uses the resource. Share
the resource with that project first.

## What sharing does not do

Sharing does not:

- transfer ownership
- grant project admin access
- authorize direct resource update/delete mutations from a non-owner project
- allow the target project to change ownership or sharing
- let project members bypass their project role; `Modify/Delete` still requires write-level access in that project
- bypass resource-specific compatibility, status, provider, or type checks

## Supported resource types

The ACL model supports ownership and sharing for:

- apps
- Kubernetes clusters
- databases
- integrations
- providers
- services
- stacks

Dashboard screens may expose these controls in different places depending on the resource type. Container-based databases are app-owned and cannot be shared independently: change their ownership and project access from the owning app's `Sharing` page. Managed databases retain their own sharing controls.

## Dashboard workflow

Open the resource and go to `Sharing`. For a container-based database, open its owning app and use the app's `Sharing` page instead.

The `Sharing settings` card has two areas:

- `Ownership` controls the resource owner.
- `Project access` controls which projects can use the resource, and whether each project-resource link is read-only or write-capable.

In `Ownership`, the `Owner` field can be:

- `Organization <organization>` for an organization-owned resource
- `Project` plus a required `Project` selector for a project-owned resource

When a resource is project-owned, the owner project is always included in project access with `Modify/Delete` access. In the dashboard table it is marked with an `Owner` tag.

In `Project access`, choose:

- `Read/Use` when the project should be able to see and select the resource
- `Modify/Delete` when the project-resource link should be write-capable where supported

For an organization-owned cluster, integration, stack, or service, `Available to` sets whether the resource is
available to `Selected projects` or to `All projects`. See
[Make a resource available to all projects](#make-a-resource-available-to-all-projects).

Click `Update` to save the owner and access list.

## Creation, import, and copy forms

For resources that support ownership on creation, including apps, the dashboard uses an `Owner` selector:

- choose `Organization <organization>` to create at organization scope
- choose `Project <project>` to create with that project as owner

Projects are grouped under `Projects` in the selector.

When the organization is the owner of a new cluster, integration, stack, or service, select
`Available to all projects` to let every project use it without sharing it project by project.

The selected owner also controls which existing organization/project-scoped resources can be referenced. This applies
when selecting a stack or cluster for an app, attaching integrations or databases, choosing a backup destination,
copying configuration, and using other resource-backed settings.

| Target owner | Resources the target can reference |
| --- | --- |
| Organization | Organization-owned resources in the same organization |
| Project | Resources in the same organization that are owned by or explicitly shared with the target's owner project, or available to all projects |

For a project-owned target, an organization-owned resource must be shared with the owner project or available to all
projects. Your personal access to the resource through organization administration or another project does not replace
that. `Read/Use` access is sufficient unless the workflow specifically requires a write-capable relationship.

For an organization-owned target, a project-owned resource is not valid even when an organization owner or admin can
access both. Move the dependency to organization ownership or choose another organization-owned dependency first.

Organizations do not need a project for organization-owned resources to work together. If an organization has no
projects, its organization-owned targets can reference organization-owned resources in the same organization without
creating project shares.

Public catalog resources and built-in Wodby services that do not use organization/project ownership continue to follow
their own availability and compatibility rules.

- Changing `Owner` clears selections that may belong to the previous scope. Select the stack, cluster, integration, or database again from the refreshed options.
- The project filter in the dashboard header controls your general working view; it does not override the target's ownership boundary on a creation form.

For example, if Project B owns a new app, a stack or cluster that only Project A can use does not appear. An
organization-owned resource that you can see but Project B cannot use is listed greyed out with a
`Not shared with the project` label. Share the resource with Project B, or make it available to all projects, then
return to the form.

## Changing sharing with active references

Sharing and ownership updates preserve the validity of existing resource relationships. An update is rejected when it
would make a referenced stack, cluster, integration, database, backup storage integration, or active CI/CD reference
invalid for the resource that uses it.

For example, Wodby rejects an update that would:

- remove the target owner project's access to a dependency
- switch a dependency from `All projects` to `Selected projects` while a project without its own share uses it
- move a target to organization ownership while it still uses a project-owned dependency
- move a dependency to project ownership while an organization-owned target still uses it
- move a project-owned target to a project where its dependency is not shared

App environment CI and registry selections are references too. A pending or active build retains its CI reference, and a
non-voided build image retains its registry reference. Backup presets and backup records retain their
storage-integration reference until those records are removed.

Before removing a project share or moving a resource to another owner project:

1. Check which apps, managed clusters, managed databases, stacks, backup presets, backups, or builds use the resource.
2. Share the dependency with the resource's new owner project, or change the dependent resource to use another compatible dependency.
3. Save the sharing or ownership update again.

This validation applies even when you personally have access to both projects. Your access allows you to perform the operation, but it does not merge the projects' resource boundaries.

## Where shared resources appear

Shared resources appear in the target project's `Resources` view and in resource selectors where the workflow supports that resource type. Resources available to all projects appear in every project's `Resources` view with `Read/Use` access.

If a resource from Project A is missing while you work in Project B, check whether:

- the resource is shared to Project B or available to all projects
- you have access to Project B
- the resource is in a usable status
- the resource type is compatible with the workflow

## Related pages

- [Projects](projects.md)
- [Access control](access-control.md)
- [Share an OAuth integration with another organization](integrations/organization-sharing.md)
