# Sharing

Projects isolate resources by default. Sharing is how a resource becomes visible or usable outside its owner scope.

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
- a platform team should let another project use a shared resource without transferring ownership

## Ownership scopes

A share never changes the resource owner.

| Ownership scope | Who can directly modify/delete the resource | Who can read/use it | Who can change ownership/sharing |
| --- | --- | --- | --- |
| Organization-owned | Organization owners/admins | Organization owners, admins, support users, and users in shared projects | Organization owners/admins |
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

Dashboard screens may expose these controls in different places depending on the resource type.

## Dashboard workflow

Open the resource and go to `Sharing`.

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

Click `Update` to save the owner and access list.

## Creation, import, and copy forms

For resources that support ownership on creation, including apps, the dashboard uses an `Owner` selector:

- choose `Organization <organization>` to create at organization scope
- choose `Project <project>` to create with that project as owner

Projects are grouped under `Projects` in the selector.

## Where shared resources appear

Shared resources appear in the target project's `Resources` view and in resource selectors where the workflow supports that resource type.

If a resource from Project A is missing while you work in Project B, check whether:

- the resource is shared to Project B
- you have access to Project B
- the resource is in a usable status
- the resource type is compatible with the workflow

## Related pages

- [Projects](projects.md)
- [Access control](access-control.md)
