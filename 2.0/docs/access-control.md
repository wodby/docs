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
- Can the user reveal a stored credential as readable text?

## Organization roles

Organization membership is the top-level access gate. A user must have an active organization membership before any project or resource access can apply.

| Role      | Meaning                                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------|
| `Owner`   | Full access to organization resources and billing. Owners can manage other owners.                                                       |
| `Admin`   | Full access to organization resources, projects, teams, and org-owned resources. Admins do not manage billing, termination protection, owners, or other admins.  |
| `Member`  | Works through project access. Members do not receive organization-wide resource access by default.                                       |
| `Support` | Read-only access across the organization.                                                                                       |
| `Robot`   | Internal automation role. Robot users are not assigned to teams or projects and are not managed through normal membership workflows.     |

Organization owners and admins have full resource access across the organization. Project roles matter most for organization members.

Support and robot users cannot be invited as normal users and cannot be assigned to teams or projects.

## Membership management

Organization membership changes follow role hierarchy rules.

- Owners can manage owners, admins, and members.
- Admins can manage members, but not owners or other admins.
- Members cannot manage organization memberships.
- Support and robot memberships are not managed through the normal organization membership UI.

An invitation sets only the email address and the organization role. Give access to projects and teams afterwards from
the member's page, `Organization > Members > [Member]`:

- `Projects` lists every project the member can access, with the role and whether the access is direct or comes from a
  team. Owners and admins can add the member to a project, change a direct role, or remove direct access. Access
  through a team is changed on the team or on the project.
- `Teams` lists the member's teams and their role in each. Owners and admins can add, remove, or change them.
- `Edit` changes the organization role or removes the member.

Invited people can be added to teams right away. Direct project access can be added once they accept the invitation.

When an organization membership is removed, Wodby also removes that membership from teams and direct project memberships.

## Teams

Teams are reusable groups of organization members. Use teams when the same people need the same project access in several places.

Team roles are:

| Role          | Meaning                                                                          |
|---------------|----------------------------------------------------------------------------------|
| `Member`      | Receives the project access given to the team.                                   |
| `Team leader` | Receives the project access given to the team, and can see the team and its members. |

Organization owners and admins can create, update, and delete teams. They also manage team members and team leaders.

A team can hold any project role except roles that manage the project: the system `Admin` role, and custom roles with
the `Manage project` permission. Project administration is only granted directly to specific organization members.

## Project roles

Projects are the main day-to-day permission boundary. Project access can be granted:

- directly to an organization member
- indirectly through one or more teams

A project role is a set of permissions. Some permissions apply to the whole project. The others apply per environment
type, so one role can, for example, deploy to staging while only viewing production. Every organization has the
environment types `Production`, `Staging`, `Test`, `Development`, and `Feature`.

Organization owners and admins have every permission in every project. Project roles matter for organization members.

### Project permissions

| Permission         | Allows                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------|
| `View project`     | Seeing the project and the resources owned by or shared with it. Every project role includes it.                          |
| `Manage resources` | Creating and changing the project's apps, clusters, stacks, services, integrations, providers, and databases, and using `Modify/Delete` shares. |
| `Manage project`   | Changing project settings and project access. Teams cannot hold roles with this permission.                               |

### Environment permissions

Environment permissions apply to app environments of the matching type. For a database that belongs to an environment,
they also decide backups, restores, deletion, and secret reveal; creating a database and changing its settings or users
needs `Manage resources`. App-wide settings, creating apps, and other project resources also need `Manage resources`.
Preview environments use the environment type configured for the app's previews.

| Permission                | Allows                                                                                                         |
|---------------------------|----------------------------------------------------------------------------------------------------------------|
| `View`                    | Seeing status, settings, deployments, metrics, and tasks.                                                      |
| `Logs`                    | Reading application logs.                                                                                      |
| `Deploy`                  | Running builds and deployments, redeploying, and cancelling them.                                              |
| `Operate`                 | Restarting, pausing, maintenance mode, running actions and crons, and controlling workspaces.                  |
| `Configure`               | Changing settings, variables, Helm values, resources, routes, ports, endpoint auth, tokens, links, integrations, and schedules. |
| `Upgrade`                 | Upgrading and reconciling the stack, and moving the environment to another cluster.                            |
| `Shell`                   | Opening the [web terminal](apps/web-terminal.md) and running commands. A shell exposes the credentials the workload receives. |
| `Back up`                 | Creating backups and backup presets, and voiding backup files.                                                 |
| `Restore`                 | Importing data, which replaces existing data.                                                                  |
| `Create`                  | Creating environments of this type.                                                                            |
| `Delete`                  | Deleting environments and databases of this type.                                                              |
| `Reveal secrets`          | Revealing app tokens, endpoint auth passwords, and database user passwords.                                    |
| `Reveal master passwords` | Revealing database master passwords.                                                                           |

Every project member can see the project's environments and read their logs, so every role includes `View` and `Logs`
in every environment type.

### System roles

Every organization has five system roles. They cannot be changed.

| Role                         | Project permissions                          | Production                                   | Other environment types                             |
|------------------------------|----------------------------------------------|----------------------------------------------|-----------------------------------------------------|
| `Read`                       | View project                                 | View, logs                                   | View, logs                                          |
| `Developer (non-production)` | View project                                 | View, logs                                   | View, logs, deploy, operate, configure, create, shell |
| `Developer`                  | View project                                 | View, logs, deploy, operate, configure, create | View, logs, deploy, operate, configure, create, shell |
| `Write`                      | View project, manage resources               | Every permission except secret reveal        | Every permission except secret reveal               |
| `Admin`                      | All                                          | All                                          | All                                                 |

`Write`, `Developer`, and `Developer (non-production)` memberships also have a `Reveal secrets` switch. See
[Secret reveal permissions](#secret-reveal-permissions).

`Organization > Project roles` lists every role with exactly what it allows in each environment type.

### Custom project roles

Organization owners and admins can define their own project roles in `Organization > Project roles`:

1. Open a role that is close to what you need and select `Copy`, or select `New project role`.
2. Set a title and a name. The name uses lowercase letters, digits, dashes, or underscores, and cannot be a system role
   name.
3. Choose the project permissions, and the environment permissions for each environment type.
4. Save the role. It can now be chosen on any project's `Access` page and on member pages.

Changing a custom role changes access at once for every member and team that holds it. A role cannot be deleted while
any project membership holds it; give those members and teams another role first. A role that teams hold cannot get
the `Manage project` permission.

Custom roles grant `Reveal secrets` and `Reveal master passwords` per environment type, so memberships with a custom
role have no separate `Reveal secrets` switch. New projects start with a system role for their first members; custom
roles can be given on the project's `Access` page afterwards.

### Combining access

A user who receives project access in more than one way gets every permission that any of those memberships grants,
for each environment type.

Example:

- direct project membership is `Developer (non-production)`
- team project membership is a custom role that can deploy and upgrade production
- the user can work in staging, development, test, and feature environments, and deploy and upgrade production

Team access never includes managing the project. Even if older data contains an admin role for a team, Wodby treats that
team role as `Write` during access checks.

### Managing project access

Project access is managed from `Organization > Projects > [Project] > Access`, or per member from
`Organization > Members > [Member] > Projects`.

Organization owners/admins and members whose role includes `Manage project` can:

- add organization members
- add teams
- assign direct user roles
- assign team roles
- change roles later
- remove project memberships

## Secret reveal permissions

Changing an app and seeing the secrets Wodby stores for it are separate permissions. This lets a developer manage and
deploy an app without automatically receiving every credential that Wodby stores for it.

For project-owned resources, direct secret reveal follows this table:

| Effective access | Reveal secrets | Reveal master passwords |
| --- | --- | --- |
| Organization owner or admin | Allowed | Allowed |
| Project `Admin` | Allowed | Allowed |
| Project `Write`, `Developer`, or `Developer (non-production)` with `Reveal secrets` turned on | Allowed in environment types the role can configure | Not allowed |
| The same roles with `Reveal secrets` turned off | Not allowed | Not allowed |
| Project `Read` | Not allowed | Not allowed |
| Custom role | As set for each environment type | As set for each environment type |

`Reveal secrets` currently covers app-service tokens, app endpoint-auth passwords, and database-user passwords.
`Reveal master passwords` covers database master or root passwords. Organization-owned secrets can be revealed only by
organization owners and admins.

The `Reveal secrets` switch is set per membership, on the project's `Access` page or the member's page. If a user has
several memberships in the same project, secret reveal is allowed when at least one of them allows it. Access through a
project that merely shares the resource does not grant direct reveal—the permission is evaluated through the resource's
owner project.

Existing `Write` assignments may initially have `Reveal secrets` turned on to preserve their previous access. Project
administrators should review those assignments from the project's `Access` page and turn it off where it is not needed.

Every direct reveal also requires an interactive user session with a recent login or step-up confirmation. Depending
on the account, Wodby asks for a password, authenticator/recovery code, or a code sent to the verified primary email.
See [Secret reveal confirmation](user/security.md#secret-reveal-confirmation).

!!! warning "Runtime access is broader than the reveal button"
    Secret reveal permission controls whether Wodby displays a stored value through its dashboard/API reveal operation.
    It does not prevent an authorized workload from receiving its configured credentials. A user who can deploy or
    configure an app, or open a [web terminal](apps/web-terminal.md), may be able to inspect credentials already
    injected into that runtime. Give deploy, configure, and shell permissions only to trusted application operators,
    even when direct secret reveal is disabled.

## Permission meanings

Wodby uses the same basic permission meanings across resource types.

| Permission               | Meaning                                                                | Typical requirement                                                                                                                                 |
|--------------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Read/use                 | View, select, or reference an existing resource in supported workflows | Any project role on the owner project or a project with `Read/Use` or `Modify/Delete` sharing, or org-wide view access where the resource is organization-owned |
| Create in project        | Create a new project-owned resource                                    | A project role with `Manage resources`, or organization owner/admin                                                                                 |
| Create in organization   | Create a new organization-owned resource                               | Organization owner/admin                                                                                                                            |
| Modify/delete            | Change or remove the resource itself                                   | Organization owner/admin for organization-owned resources. For project-owned resources, `Manage resources` in the owner project, or the matching [environment permission](#environment-permissions) for app environments and their databases |
| Ownership & sharing      | Change the resource owner or project access list                       | See [Resource ownership](#resource-ownership). The requirement depends on whether the resource is organization-owned or project-owned                 |
| Manage project           | Rename, delete, or manage project access                               | A project role with `Manage project`, or organization owner/admin                                                                                   |
| Manage organization/team | Manage org settings, teams, team members, team leaders, and custom project roles | Organization owner/admin                                                                                                                  |
| Manage termination protection | Change organization-wide deletion safeguards                       | Organization owners only                                                                                                                           |
| Manage org members       | Invite, change roles, or remove organization members                   | Owners can manage owners/admins/members. Admins can manage members only                                                                             |
| Manage billing           | Change subscription, billing details, invoices, or spending limits      | Organization owners only                                                                                                                           |

## What read means

In Wodby, read access is not only inspection. For reusable resources, read access also means use access.

For example, if a user can create an app in Project A and Project A can read a cluster, stack, integration, service, provider, or database, that resource can be selected where the workflow allows it.

Typical read/use examples:

- deploy an app to a visible Kubernetes cluster
- create an app from a visible stack
- attach a visible integration to an app service
- use a visible service, provider, or database in a supported workflow

The user still needs write access to the target object they are creating or modifying. For example, deploying an app requires write access in the app's project even if the selected cluster only needs read/use access.

Resource-specific checks still apply. A resource may need to be in an `OK` status, belong to the same organization, provide the right integration type, or satisfy stack/service compatibility rules.

Read/use access for the user is necessary but does not by itself make an organization/project-scoped resource a valid
dependency. A project-owned target can reference resources owned by or shared with its owner project, and
organization-owned resources that are available to all projects. An organization-owned target can reference only
organization-owned resources in the same organization. See [Sharing](sharing.md#creation-import-and-copy-forms).

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

| Action              | Allowed users                                                                                     |
|---------------------|---------------------------------------------------------------------------------------------------|
| Read/use            | Organization owners, admins, support users, or users who can access a project with `Read/Use` or `Modify/Delete` access. Every organization member when the resource is available to all projects |
| Modify/delete       | Organization owners and admins                                                                    |
| Ownership & sharing | Organization owners and admins                                                                    |

Regular organization members do not automatically see organization-owned resources. They can see and use an organization-owned resource only when it is shared with a project they can access or when it is [available to all projects](sharing.md#make-a-resource-available-to-all-projects).

### Project-owned resources

Project-owned resources have one owner project. The owner project always has `Modify/Delete` access, and additional projects can receive either `Read/Use` or `Modify/Delete` access through sharing.

Access rules:

| Action              | Allowed users                                                                                              |
|---------------------|------------------------------------------------------------------------------------------------------------|
| Read/use            | Users who can access the owner project or any shared project                                               |
| Modify/delete       | Users whose role in the owner project includes `Manage resources`, plus organization owners/admins. App environments and their databases follow the [environment permissions](#environment-permissions) |
| Ownership & sharing | Organization owners/admins. For project-owned resources that remain project-owned, users with owner-scope write access can update sharing or owner project when they also have project `Admin` access to every affected project |

Sharing a project-owned resource to another project does not move ownership. A `Read/Use` share grants visibility and use only. A `Modify/Delete` share includes read/use and marks the project-resource link as write-capable for project-scoped ACL checks, but direct resource update/delete mutations still require access through the owner project or organization admin/owner access.

## Sharing

Sharing makes a resource visible or usable outside its owner scope. A `Modify/Delete` share also marks the project-resource link as write-capable for workflows that check project-resource access.

Use sharing when:

- several projects should deploy to the same Kubernetes cluster
- several projects should use the same integration
- one project should consume a stack, service, provider, or database owned elsewhere
- an organization-owned resource should be available to selected project members

Sharing does not grant project administration rights and does not transfer ownership.

Project access entries have two access levels:

- `Read/Use` lets the target project view, select, or reference the resource.
- `Modify/Delete` includes `Read/Use` and marks the project-resource link as write-capable for workflows that check project-resource access.

For organization-owned resources, only organization owners and admins can change the resource owner or project access list. Changing any resource to organization ownership also requires organization owner/admin access. For project-owned resources that remain project-owned, a user must have resource write access through the owner scope and `Admin` access to each project whose share or owner is changed. Organization owners and admins satisfy these checks across the organization.

See [Sharing](sharing.md) for the user-facing sharing workflow.

## Tasks

Tasks inherit access from the resources and projects they reference.

- Project-linked tasks are visible through their linked projects.
- A task linked to several projects is visible if the user can access at least one linked project.
- Project-linked tasks can be repeated by organization owners/admins and project members who can access at least one linked project.
- Project-linked tasks can be cancelled or otherwise modified only by organization owners and admins.
- Project-linked tasks do not fall back to general organization membership if the user cannot access any linked project.
- Tasks without project links are treated as organization-scoped tasks.

Organization-scoped tasks can be read by roles with organization-wide visibility. They can be repeated, cancelled, or otherwise modified only by organization owners and admins.

## Apps and app environments

Apps can be organization-owned or project-owned. In the dashboard, the app creation `Owner` field accepts either `Organization <organization>` or `Project <project>`. Creating an organization-owned app requires organization owner/admin access. Creating a project-owned app requires write/admin access in the owner project, or organization owner/admin access.

During app creation, referenced resources such as clusters, stacks, integrations, services, providers, and databases
generally require read/use access, not modify access. A shared cluster can therefore be a valid deployment target for a
project-owned app without granting cluster write access, provided the cluster is shared with the app's owner project.
Organization/project-scoped dependencies for an organization-owned app must be organization-owned in the same
organization.

App environments do not have a separate project owner. They belong to the app and use the app's ownership and sharing settings. Container-based databases created for app services follow the same rule: their owner and project access list stay synchronized with the app and cannot be changed independently. Managed databases keep their own ownership and sharing settings.

Changing an existing app, app environment, app service, deployment, build source, environment variables, tokens, annotations, routes, ports, auth settings, and similar app-owned configuration requires modify access to the app or app environment.

## Practical examples

### Shared cluster

Project Platform owns a Kubernetes cluster. Project Web can read/use that cluster through a `Read/Use` share.

- A Project Web writer can deploy an app from Project Web to the shared cluster.
- The same user cannot scale or delete the cluster unless they also have write/admin access to the owner project or organization admin/owner access.
- The same user cannot change ownership or sharing unless they have owner-scope write access and `Admin` access to the affected projects, or organization admin/owner access. Changing the cluster to organization ownership requires organization admin/owner access.

### Organization-owned integration

An organization admin creates a GitHub integration at organization scope and shares it with Project API as `Read/Use`.

- Project API users can select the integration in supported workflows.
- Only organization owners and admins can modify or delete the integration.

### Team access

A `Developers` team is added to Project App with `Write`.

- Team members can create and update resources inside Project App.
- Team leaders can view the `Developers` team, but organization owners/admins manage team membership.
- The team cannot be project admin. Project admin must be granted directly to specific users.

### Production changes by a few people

Only system administrators should deploy to and patch production. Core developers work freely outside production and
only look at production. One team works on a single project, and its leads manage that project's access.

1. Create a custom role `Sys admin` by copying `Read` and adding `Deploy`, `Operate`, `Configure`, `Upgrade`,
   `Back up`, and `Restore` in `Production`. Give it to a `Sys admins` team in every project.
2. Give a `Core developers` team the `Developer (non-production)` role in the same projects. Leave `Delete` out by
   using the system role, or copy it into a custom role to fine-tune it.
3. Give a `Team X` team the `Developer` or `Developer (non-production)` role in Team X's project only.
4. Give Team X's leads a custom role with `Manage project` directly in that project, so they can manage its access.
   Teams cannot hold that permission.

## Related pages

- [Organization](org.md)
- [Projects](projects.md)
- [Teams](teams.md)
- [Sharing](sharing.md)
