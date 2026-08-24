# Organization

## Overview

An organization is the top-level scope for your users, teams, projects, shared defaults, and billing.

Day-to-day resources such as apps, Kubernetes clusters, databases, integrations, services, and providers are used through [projects](projects.md), while organization-level pages are used to manage the overall workspace.

An organization has a title, a machine name, and a default time zone. The machine name cannot be changed and may contain only lowercase letters `a-z`, numbers `0-9`, and a hyphen. It is used in technical domains for your application instances and Kubernetes clusters, and in the repository namespace of Wodby Registry.

When an organization is created, the dashboard preselects the creator's browser time zone and lets them change it before
creation. If browser time zone detection is unavailable, Wodby uses `UTC`. The default supplies the time zone for new
[automation time windows](automation-time-windows.md); changing it does not alter windows already stored on resources.

### Roles

Organization members have one of the following roles:

- **Owners** have full access to all resources and billing
- **Admins** have full access to all resources and can view, but not manage, billing
- **Members** have access to resources in projects they are added to directly or through teams
- **Support** users have read-only access across the organization
- **Robot** users are internal automation users and are not assigned to teams or projects

In the dashboard, organization-level administration is handled by owners and admins. Members typically work from project-scoped areas such as apps, clusters, databases, integrations, stacks, services, providers, and tasks.

## Invitation

You can invite users by email whether they already have a Wodby account or not. The invitation link is valid for 3 days. If the invited person does not have an account yet, they are prompted to create one after opening the link.

## Organization navigation

The organization area in the dashboard includes these sections:

- `Members` to invite users, review membership status, and manage organization roles
- `Projects` to create projects, review project resources, and manage project access
- `Teams` to group users and reuse project access assignments
- `Environments` to manage named environments used by apps and databases
- `Backups` to create organization-wide backup presets reused in app and database backup flows
- `Certificates` to review issued certificates used by application routes and supported database resources
- `SSO` to configure organization-level Single Sign-On providers
- `Billing` for subscription and plan-related operations
- `Settings` to manage organization-wide defaults
- `Edit` to review and edit the organization record or delete the organization

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

## Billing

Billing is managed at the organization level.

See [Billing](pricing.md) for the current plan model and Wodby Cloud billing notes.

## Settings

`Organization > Settings` manages defaults used when creating resources. From there you can change:

- the default time zone
- the default CI provider
- the default container registry
- organization-wide termination protection

The CI and registry selectors include Wodby's built-in services and available organization-owned integrations of the
corresponding type. Project-owned integrations cannot be used as organization defaults because they may not be
available to apps in other projects.

The selected CI and registry initialize new apps and new app instances. Each app instance stores CI as its Default CI
for connected build sources and stores the registry as its instance-wide selection. Changing an organization default
does not change existing instances or historical builds. Public and cloned boilerplate sources use Wodby CI regardless
of Default CI. The selections are retained when an instance has no enabled service with build configuration, allowing
a buildable service to be enabled or added later without changing the intended providers.

Choose `Wodby CI` or `Wodby US Docker Registry` to use the corresponding built-in service as the organization default.

### Termination protection

Termination protection adds an organization-wide safeguard against destructive operations. It applies after the usual
access and dependency checks, so disabling it does not grant anyone permission to delete resources.

Only an organization owner can change the setting. Enabling, changing, or disabling it requires a recent interactive
security confirmation. Depending on the account, Wodby asks for a password, an authenticator or recovery code, or a
code sent to the verified primary email address. A successful login or step-up confirmation remains recent for 5
minutes. API keys and other non-interactive credentials cannot change the setting. Wodby sends the organization's
owners a security notification after it changes.

| Mode | Apps and clusters | Databases | Integrations, services, stacks, and providers |
| --- | --- | --- | --- |
| `Disabled` | No additional deletion blocks | No additional deletion blocks | No additional deletion blocks |
| `Production` | Blocks deleting a non-infrastructure app instance in a `prod` environment. It also blocks deleting an app or cluster when that operation would delete such an instance. | Blocks deleting a database server in a `prod` environment or an individual DB inside it. | Blocks deleting integrations. Services, stacks, and providers remain deletable. |
| `All` | Blocks deleting every cluster and every non-infrastructure app instance. It also blocks deleting an app when that operation would delete one or more such instances. | Blocks deleting every database server and every individual DB. | Blocks deleting integrations, services, stacks, and providers. |

The `Production` mode uses the environment's type, not its display name. An environment that is named “Production”
but has another type is not protected by this mode. Wodby also prevents changing the type of an environment while an
app instance or database references it, so a protected resource cannot be reclassified before deletion.

Protection applies to deletion requests from both the dashboard and API, and a force-delete option does not bypass it.
It also applies when another operation would delete a protected resource, such as a stack upgrade that removes an
app-owned database. Deletion workflows that already started before protection was enabled can finish.

!!! note "Demo clusters still expire"
    Temporary Wodby Cloud demo clusters are deleted automatically after 24 hours, together with their applications,
    even when termination protection is set to `All`.

## Editing the organization

`Organization > Edit` manages the organization record itself.

From there you can:

- review the organization ID
- review join date
- review the machine name
- change the organization title
- delete the organization

## Single Sign-On

Organization owners and admins can configure Single Sign-On providers for the organization. Enabling providers and
signing in with organization SSO require an active paid subscription.

SSO lets users sign in through your identity provider, such as Okta, Microsoft Entra ID, Google Workspace, GitHub, Auth0, ZITADEL, Keycloak, or a SAML identity provider. It is currently an additional sign-in option and does not disable existing sign-in methods or API keys.

See [Single Sign-On](sso.md) for setup, domain verification, and login behavior.

## Related pages

- [Projects](projects.md)
- [Teams](teams.md)
- [Access control](access-control.md)
- [Single Sign-On](sso.md)
- [Billing](pricing.md)
