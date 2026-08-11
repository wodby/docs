# Projects

Projects are the main isolation boundary inside your [organization](org.md).

You use projects to:

- group related apps, clusters, databases, integrations, stacks, services, and providers
- control who can see or change those resources
- keep environments or teams separated inside the same organization

Resources can be project-owned or organization-owned. Project-owned resources have one owner project and can be shared with additional projects when needed. Organization-owned resources can also be shared to projects so regular project members can use them.

## Project pages

Each project has three main areas:

- `Resources` lists everything visible in the project
- `Access` controls which organization members and teams can use the project
- `Edit` lets you rename or delete the project

The `Resources` page can include:

- apps
- Kubernetes clusters
- databases
- integrations
- stacks
- services
- providers

Shared resources can appear here even when they are owned by another project or by the organization. Depending on the share level, the project may have `Read/Use` or `Modify/Delete` access.

## Creating a project

Create projects from `Organization > Projects`.

Projects are available on all active plans, with no plan-based limit on the number of projects in an organization.

When creating a project, you can:

- set the project name
- optionally preselect organization members
- optionally preselect teams
- choose one initial role for those selected users or teams
- when the initial role is `Write`, choose whether those memberships can reveal runtime secrets

Project creation itself is an organization-level action, so it is typically handled by organization owners or admins.

## Project filter

The project selector in the dashboard header is your working scope.

- You can select one or more projects.
- `Select all` is available when you want to work across the whole organization.
- At least one project must remain selected.
- Your selection is stored as your default project filter for that organization.

This filter affects the lists you see across project-aware areas such as apps, clusters, databases, integrations, stacks, services, providers, and tasks.

## Access model

Access is granted per project, either:

- directly to an organization member
- through a team added to the project

Project roles are:

- `Read` to view the project and use resources visible in it
- `Write` to create and modify resources inside the project
- `Admin` to manage the project itself

Teams can receive `Read` or `Write` project roles. Project `Admin` is granted directly to specific users.

For `Write` memberships, project administrators can independently enable or disable `Reveal runtime secrets`. This
controls direct display of app-service tokens, endpoint-auth passwords, and database-user passwords. Project `Admin`
includes secret reveal, while `Read` cannot receive it. See
[Secret reveal permissions](access-control.md#secret-reveal-permissions).

See [Access control](access-control.md) for the full role model.

## Resource boundaries

Projects are also resource boundaries.

- Resources from one project are not automatically available in another.
- Cross-project references are not allowed unless the resource is explicitly shared to the target project.
- Organization-owned dependencies that use project sharing must also be explicitly shared before a project-owned target can reference them.
- An organization-owned target can reference only organization-owned resources in the same organization when the dependency uses organization/project ownership; access to a project-owned resource does not make it valid for that target.
- Write-capable project-resource workflows require a `Modify/Delete` share and write-level access in the target project where that workflow supports shared-resource writes.
- Direct resource update/delete operations still follow the resource owner scope.
- Organization-owned resources are visible to regular project members only when shared to one of their projects.
- For example, a project-owned app cannot use an organization/project-scoped cluster, database, integration, service, stack, or provider unless that resource is owned by or shared with the app's owner project.
- On creation forms, the selected resource owner defines this context. If Project B owns the new resource, referenced resources must be owned by or shared with Project B. Selecting Project A in the dashboard header does not make Project A-only resources valid for a Project B-owned resource.
- Changing a resource owner or removing project access is rejected when that change would leave an existing app, cluster, database, stack, integration, or backup preset with an inaccessible dependency. Update the dependent resource or share its dependency with the new owner project first.

See [Sharing](sharing.md) for how cross-project visibility works in practice.

## Deleting a project

A project cannot be deleted while it still contains resources. Remove dependent resources first, then delete the project.

## Related pages

- [Organization](org.md)
- [Teams](teams.md)
- [Access control](access-control.md)
- [Sharing](sharing.md)
