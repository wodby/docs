# Projects

Projects are the main isolation boundary inside your [organization](org.md).

You use projects to:

- group related apps, clusters, databases, integrations, stacks, services, and providers
- control who can see or change those resources
- keep environments or teams separated inside the same organization

Resources can be project-owned or organization-owned. Project-owned resources have one owner project and can be shared with additional projects when needed. Organization-owned resources can also be shared to projects so regular project members can use them. An organization-owned cluster, integration, stack, or service can be [available to all projects](sharing.md#make-a-resource-available-to-all-projects) instead.

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

Shared resources can appear here even when they are owned by another project or by the organization. Depending on the share level, the project may have `Read/Use` or `Modify/Delete` access. Organization-owned resources that are available to all projects appear in every project with `Read/Use` access.

## Creating a project

Create projects from `Organization > Projects`.

Projects are available on all active plans, with no plan-based limit on the number of projects in an organization.

When creating a project, you can:

- set the project name
- optionally preselect organization members
- optionally preselect teams
- choose one initial system role for those selected users or teams
- for `Write` and the `Developer` roles, choose whether those memberships can reveal secrets

Custom project roles can be given on the project's `Access` page after the project is created.

Project creation itself is an organization-level action, so it is typically handled by organization owners or admins.

## Project filter

The project selector in the dashboard header sets the project you are working in. You work in one project at a time, so to compare projects, switch between them.

- Lists of apps, clusters, databases, integrations, stacks, services, providers, and tasks follow the selected project. Resource lists also include resources shared with that project and organization-owned resources you can view.
- Creation forms start with the selected project as the owner when you can create resources in it. You can choose another owner on the form.
- Your selection is saved as your default for that organization. Until you pick one, the dashboard starts on the organization's oldest project. If you had selected several projects before, it starts on the oldest of them.
- If you open a resource the selected project cannot see, for example from a link, the selector switches to the resource's project. Your saved default does not change.

## Access model

Access is granted per project, either:

- directly to an organization member
- through a team added to the project

Each membership has a [project role](access-control.md#project-roles). A role grants project-wide permissions and
permissions per environment type, so you can, for example, let developers deploy to staging while only sysadmins
deploy to production. The system roles are:

- `Read` to view the project, its environments, and their logs
- `Developer (non-production)` to work in every environment type except production, which stays read-only
- `Developer` to deploy, operate, configure, and create environments of every type, with a shell outside production
- `Write` to create and modify resources inside the project
- `Admin` to manage the project itself

Organization owners and admins can also create custom project roles. Teams cannot receive roles that manage the
project; project administration is granted directly to specific users.

For `Write` and the `Developer` roles, project administrators can turn `Reveal secrets` on or off per membership. This
controls direct display of app-service tokens, endpoint-auth passwords, and database-user passwords. See
[Secret reveal permissions](access-control.md#secret-reveal-permissions).

See [Access control](access-control.md) for the full role model.

## Resource boundaries

Projects are also resource boundaries.

- Resources from one project are not automatically available in another.
- Cross-project references are not allowed unless the resource is explicitly shared to the target project.
- Organization-owned dependencies that use project sharing must also be shared with the project, or available to all projects, before a project-owned target can reference them.
- An organization-owned target can reference only organization-owned resources in the same organization when the dependency uses organization/project ownership; access to a project-owned resource does not make it valid for that target.
- Write-capable project-resource workflows require a `Modify/Delete` share and write-level access in the target project where that workflow supports shared-resource writes.
- Direct resource update/delete operations still follow the resource owner scope.
- Organization-owned resources are visible to regular project members only when shared to one of their projects or available to all projects.
- For example, a project-owned app cannot use an organization/project-scoped cluster, database, integration, service, stack, or provider unless that resource is owned by or shared with the app's owner project, or available to all projects.
- On creation forms, the selected resource owner defines this context. If Project B owns the new resource, referenced resources must be owned by or shared with Project B. Selecting Project A in the dashboard header does not make Project A-only resources valid for a Project B-owned resource.
- Changing a resource owner or removing project access is rejected when that change would leave an existing app, cluster, database, stack, integration, or backup preset with an inaccessible dependency. Update the dependent resource or share its dependency with the new owner project first.

See [Sharing](sharing.md) for how cross-project visibility works in practice.

## Deleting a project

A project cannot be deleted while it still contains resources. Remove dependent resources first, then delete the project.

Every organization keeps at least one project, so its last project cannot be deleted. Create another project first if
you want to replace it. Deleting the whole organization removes all of its projects.

## Related pages

- [Organization](org.md)
- [Teams](teams.md)
- [Access control](access-control.md)
- [Sharing](sharing.md)
