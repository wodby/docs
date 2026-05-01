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

Shared resources can appear here even when they are owned by another project or by the organization.

## Creating a project

Create projects from `Organization > Projects`.

When creating a project, you can:

- set the project name
- optionally preselect organization members
- optionally preselect teams
- choose one initial role for those selected users or teams

Project creation itself is an organization-level action, so it is typically handled by organization owners or admins.

## Project filter

The project selector in the dashboard header is your working scope.

- You can select one or more projects.
- `Select all` is available when you want to work across the whole organization.
- At least one project must remain selected.
- Your selection is stored as your default project filter for that organization.

This filter affects the lists you see across project-aware areas such as apps, Kubernetes, databases, integrations, stacks, services, providers, and tasks.

## Access model

Access is granted per project, either:

- directly to an organization member
- through a team added to the project

Project roles are:

- `Read` to view the project and use resources visible in it
- `Write` to create and modify resources inside the project
- `Admin` to manage the project itself

Teams can receive `Read` or `Write` project roles. Project `Admin` is granted directly to specific users.

See [Access control](access-control.md) for the full role model.

## Resource boundaries

Projects are also resource boundaries.

- Resources from one project are not automatically available in another.
- Cross-project references are not allowed unless the resource is explicitly shared to the target project.
- Organization-owned resources are visible to regular project members only when shared to one of their projects.
- For example, an app cannot use a cluster, database, integration, service, stack, or provider from another project unless that resource is visible in the app's project context.

See [Sharing](sharing.md) for how cross-project visibility works in practice.

## Deleting a project

A project cannot be deleted while it still contains resources. Remove dependent resources first, then delete the project.

## Related pages

- [Organization](org.md)
- [Teams](teams.md)
- [Access control](access-control.md)
- [Sharing](sharing.md)
