# Projects

Projects are the main isolation boundary inside your [organization](org.md).

You use projects to:

- group related apps, clusters, databases, integrations, stacks, services, and providers
- control who can see or change those resources
- keep environments or teams separated inside the same organization

Most resources are created in a single project first. Some resource types can later be shared with additional projects when needed.

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

If a resource is shared into the project as read-only, the project resource list shows that as `Read only`.

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

- `Read` to view the project and its resources
- `Write` to modify resources inside the project
- `Admin` to manage the project itself

See [Access control](access-control.md) for the full role model.

## Resource boundaries

Projects are also resource boundaries.

- Resources from one project are not automatically available in another.
- Cross-project references are not allowed unless the resource is explicitly shared to the target project.
- For example, an app cannot use a cluster, database, integration, service, stack, or provider from another project unless that resource is visible in the app's project context.

See [Sharing](sharing.md) for how cross-project visibility works in practice.

## Deleting a project

A project cannot be deleted while it still contains resources. Remove dependent resources first, then delete the project.

## Related pages

- [Organization](org.md)
- [Teams](teams.md)
- [Access control](access-control.md)
- [Sharing](sharing.md)
