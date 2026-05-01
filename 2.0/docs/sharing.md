# Sharing

Projects isolate resources by default. Sharing is how a resource becomes visible and usable outside its owner scope.

Sharing works together with [access control](access-control.md):

- ownership decides who can modify a resource
- sharing decides where the resource can be seen and used

## What sharing does

Sharing makes a resource available in one or more projects without moving ownership.

This is useful when, for example:

- several projects should deploy apps to the same Kubernetes cluster
- one project should use an integration managed by another project or by the organization
- multiple projects should use the same stack, service, provider, or database
- an organization-owned resource should be available only to selected projects

## Ownership scopes

A share never changes the resource owner.

| Ownership scope | Who can modify the resource | Who can read/use it |
| --- | --- | --- |
| Organization-owned | Organization owners and admins | Organization owners, admins, support users, and users in shared projects |
| Project-owned | Users with `Write` or `Admin` access to the owner project, plus organization owners and admins | Users who can access the owner project or any shared project |

Project shares grant visibility and use. They do not grant management rights over the shared resource.

## Read/use access

Read access to a shared resource means the resource can be selected or referenced by supported workflows.

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
- allow the target project to modify an organization-owned resource
- allow the target project to modify a project-owned resource owned by another project
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
