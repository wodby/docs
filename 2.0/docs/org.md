# Organization

## Overview

An organization is the top-level scope for your users, teams, projects, shared defaults, and billing.

Day-to-day resources such as apps, Kubernetes clusters, databases, integrations, services, and providers are used through [projects](projects.md), while organization-level pages are used to manage the overall workspace.

An organization has a title and a machine name. The machine name cannot be changed and may contain only lowercase letters `a-z`, numbers `0-9`, and a hyphen. It is used in technical domains for your application instances and Kubernetes clusters, and in the repository namespace of Wodby Registry.

### Roles

Organization members have one of the following roles:

- **Owners** have full access to all resources and billing
- **Admins** have full access to all resources but not billing
- **Members** have access to resources in projects they are added to directly or through teams
- **Support** users have view-only support access across the organization and billing view access
- **Robot** users are internal automation users and are not assigned to teams or projects

In the dashboard, organization-level administration pages are intended for owners and admins. Members typically work from project-scoped areas such as apps, Kubernetes, databases, integrations, stacks, services, providers, and tasks.

## Invitation

You can invite users by email whether they already have a Wodby account or not. The invitation link is valid for 3 days. If the invited person does not have an account yet, they are prompted to create one after opening the link.

## Organization navigation

The organization area in the dashboard includes these sections:

- `Members` to invite users, review membership status, and manage organization roles
- `Projects` to create projects, review project resources, and manage project access
- `Teams` to group users and reuse project access assignments
- `Environments` to manage named environments used by apps and databases
- `Backups` to manage organization-wide backup presets
- `Certificates` to review issued certificates used by supported resources
- `Billing` for subscription and plan-related operations
- `Settings` to edit the organization itself

## Members

`Organization > Members` is where you manage organization membership.

- invite users by email
- review invitation and join status
- change organization roles
- remove members when needed

See [Access control](access-control.md) for how organization roles interact with project access.

## Projects and teams

Projects and teams are the main access-management tools inside an organization.

- [Projects](projects.md) define resource boundaries
- [Teams](teams.md) help you assign access repeatedly
- [Access control](access-control.md) explains how roles are evaluated
- [Sharing](sharing.md) explains how resources can cross project boundaries safely

## Environments

Environments are managed from `Organization > Environments`.

They are shared organization-level definitions that apps, databases, and other workflows can reference. See [Environment](apps/env.md) for details.

## Backups

`Organization > Backups` focuses on organization-wide backup presets.

Those presets can be reused in app and database backup flows, and can optionally be limited to a specific environment.

See [Backups](backups.md) for the full model.

## Certificates

`Organization > Certificates` shows issued certificates and where they are used.

Custom certificate upload is coming soon.

See [Certificates](certs.md) for the current certificate model and planned direction.

## Billing

Billing is managed at the organization level.

See [Pricing & Billing](pricing.md) for the current plan model and Wodby Cloud billing notes.

## Settings

`Organization > Settings` is the page for editing the organization record itself.

From there you can:

- review the organization ID
- review join date
- review the machine name
- change the organization title
- delete the organization

## Related pages

- [Projects](projects.md)
- [Teams](teams.md)
- [Access control](access-control.md)
- [Backups](backups.md)
- [Certificates](certs.md)
- [Pricing & Billing](pricing.md)
