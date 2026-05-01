# Access control

Wodby access is layered. A user can have:

- an organization role
- one or more team memberships
- one or more direct project memberships
- project access inherited from teams

These layers answer different questions:

- Can the user enter the organization?
- Can the user administer organization-wide settings?
- Can the user see, create, or change resources in a project?
- Can the user use a resource that belongs to another project or to the organization?

## Organization roles

Organization membership is the top-level access gate. A user must have an active organization membership before any project or resource access can apply.

| Role      | Meaning                                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------|
| `Owner`   | Full access to organization resources and billing. Owners can manage other owners.                                                       |
| `Admin`   | Full access to organization resources, projects, teams, and org-owned resources. Admins do not manage billing, owners, or other admins.  |
| `Member`  | Works through project access. Members do not receive organization-wide resource access by default.                                       |
| `Support` | View-only organization-wide support access. Support users can view billing but cannot modify resources, projects, teams, or memberships. |
| `Robot`   | Internal automation role. Robot users are not assigned to teams or projects and are not managed through normal membership workflows.     |

Organization owners and admins have full resource access across the organization. Project roles matter most for organization members.

Support and robot users cannot be invited as normal users and cannot be assigned to teams or projects.

## Membership management

Organization membership changes follow role hierarchy rules.

- Owners can manage owners, admins, and members.
- Admins can manage members, but not owners or other admins.
- Members cannot manage organization memberships.
- Support and robot memberships are not managed through the normal organization membership UI.

When an organization membership is removed, Wodby also removes that membership from teams and direct project memberships.

## Teams

Teams are reusable groups of organization members. Use teams when the same people need the same project access in several places.

Team roles are:

| Role          | Meaning                                                            |
|---------------|--------------------------------------------------------------------|
| `Member`      | Regular team member. Receives project access assigned to the team. |
| `Team leader` | Can manage regular members in that team.                           |

Team leaders can add and remove regular team members in teams they lead. They cannot add, remove, promote, or demote team leaders unless they also have an organization owner or admin role.

Organization owners and admins can manage all teams and team leaders. Only organization owners and admins can delete teams.

Teams can be added to projects with `Read` or `Write` access. Teams cannot be assigned the project `Admin` role. Project administration is only granted directly to specific organization members.

## Project roles

Projects are the main day-to-day permission boundary. Project access can be granted:

- directly to an organization member
- indirectly through one or more teams

Project roles are:

| Role    | Meaning                                                                                                                                            |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `Read`  | View the project and resources visible in it. `Read` also means the resource can be selected or referenced by workflows that only need use access. |
| `Write` | Create and modify resources inside the project. `Write` includes `Read`.                                                                           |
| `Admin` | Manage the project itself, including project access and project settings. `Admin` includes `Write`.                                                |

If a user receives project access more than one way, Wodby uses the highest effective role.

Example:

- direct project membership is `Read`
- team project membership is `Write`
- effective project role is `Write`

Team-derived project access is capped at `Write`. Even if older data contains an admin role for a team, Wodby treats that team role as `Write` during access checks.

Project access is managed from `Organization > Projects > [Project] > Access`.

From there, organization owners/admins and project admins can:

- see project memberships
- add organization members
- add teams
- assign direct user roles
- assign team roles
- change roles later
- remove project memberships

## Permission meanings

Wodby uses the same basic permission meanings across resource types.

| Permission               | Meaning                                                                | Typical requirement                                                                |
|--------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Read/use                 | View, select, or reference an existing resource in supported workflows | Project `Read`, a resource share to an accessible project, or org-wide view access |
| Create in project        | Create a new project-owned resource                                    | Project `Write` or `Admin`, or organization owner/admin                            |
| Create in organization   | Create a new organization-owned resource                               | Organization owner/admin                                                           |
| Modify                   | Change resource settings or mutable configuration                      | Resource owner write access, or organization owner/admin                           |
| Delete                   | Remove the resource                                                    | Same owner-level access as modify, plus resource-specific dependency checks        |
| Share                    | Change ownership scope or project shares                               | Same owner-level access as modify                                                  |
| Manage project           | Rename, delete, or manage project access                               | Project `Admin`, or organization owner/admin                                       |
| Manage organization/team | Manage org settings, teams, and team leaders                           | Organization owner/admin, except limited team-leader member management             |
| Manage org members       | Invite, change roles, or remove organization members                   | Owners can manage owners/admins/members. Admins can manage members only            |

## What read means

In Wodby, `Read` is not only inspection. For reusable resources, read access also means use access.

For example, if a user can create an app in Project A and Project A can read a cluster, stack, integration, service, provider, or database, that resource can be selected where the workflow allows it.

Typical read/use examples:

- deploy an app to a visible Kubernetes cluster
- create an app from a visible stack
- attach a visible integration to an app service
- use a visible service, provider, or database in a supported workflow

The user still needs write access to the target object they are creating or modifying. For example, deploying an app requires write access in the app's project even if the selected cluster only needs read/use access.

Resource-specific checks still apply. A resource may need to be in an `OK` status, belong to the same organization, provide the right integration type, or satisfy stack/service compatibility rules.

## Resource ownership

Resources can be owned at either organization scope or project scope.

Supported owned resource types include:

- apps
- Kubernetes clusters
- databases
- integrations
- providers
- services
- stacks

### Organization-owned resources

Organization-owned resources belong to the organization rather than to one owner project.

Access rules:

| Action              | Allowed users                                                                                             |
|---------------------|-----------------------------------------------------------------------------------------------------------|
| Read/use            | Organization owners, admins, support users, or users who can access a project the resource is shared with |
| Modify/delete/share | Organization owners and admins                                                                            |

Regular organization members do not automatically see organization-owned resources. They can see and use an organization-owned resource only when it is shared with a project they can access.

### Project-owned resources

Project-owned resources have one owner project. The owner project controls write access.

Access rules:

| Action              | Allowed users                                                                                  |
|---------------------|------------------------------------------------------------------------------------------------|
| Read/use            | Users who can access the owner project or any project the resource is shared with              |
| Modify/delete/share | Users with `Write` or `Admin` access to the owner project, plus organization owners and admins |

Sharing a project-owned resource to another project grants visibility and use in that target project. It does not move ownership and does not let the target project manage the resource.

## Sharing

Sharing makes a resource visible and usable outside its owner scope.

Use sharing when:

- several projects should deploy to the same Kubernetes cluster
- several projects should use the same integration
- one project should consume a stack, service, provider, or database owned elsewhere
- an organization-owned resource should be available to selected project members

Sharing does not grant project administration rights and does not transfer ownership.

The owner still controls modifications:

- organization-owned resources are modified by organization owners/admins
- project-owned resources are modified by users with write/admin access to the owner project

See [Sharing](sharing.md) for the user-facing sharing workflow.

## Tasks

Tasks inherit access from the resources and projects they reference.

- Project-linked tasks are visible through their linked projects.
- A task linked to several projects is visible if the user can access at least one linked project.
- Project-linked tasks do not fall back to general organization membership if the user cannot access any linked project.
- Tasks without project links are treated as organization-scoped tasks.

Organization-scoped tasks can be read by organization owners, admins, and support users. They can be repeated or otherwise modified only by organization owners and admins.

## Apps and app instances

Apps are created in a project. Creating an app requires write-level access in the target project.

During app creation, referenced resources such as clusters, stacks, integrations, services, providers, and databases generally require read/use access, not modify access. This is why a shared cluster can be a valid deployment target for a user who has write access to the app's project.

Changing an existing app, app instance, app service, deployment, build source, environment variables, tokens, annotations, domains, ports, auth settings, and similar app-owned configuration requires modify access to the app or app instance.

## Practical examples

### Shared cluster

Project Platform owns a Kubernetes cluster. Project Web can read/use that cluster through a share.

- A Project Web writer can deploy an app from Project Web to the shared cluster.
- The same user cannot scale, delete, or change sharing for the cluster unless they also have write/admin access to the owner project or organization admin/owner access.

### Organization-owned integration

An organization admin creates a GitHub integration at organization scope and shares it with Project API.

- Project API users can select the integration in supported workflows.
- Only organization owners and admins can modify or delete the integration.

### Team access

A `Developers` team is added to Project App with `Write`.

- Team members can create and update resources inside Project App.
- Team leaders can manage regular members in the `Developers` team.
- The team cannot be project admin. Project admin must be granted directly to specific users.

## Related pages

- [Organization](org.md)
- [Projects](projects.md)
- [Teams](teams.md)
- [Sharing](sharing.md)
