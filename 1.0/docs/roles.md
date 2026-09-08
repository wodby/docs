# Permissions

Wodby roles form the following hierarchy:

`Owner` > `Administrator` > `Team leader` > `Developer` > `Unprivileged`

Each role inherits the permissions of every role to its right. The tables below
show the lowest role that receives a permission; every more privileged role
receives it as well.

## Organization permissions

| Action | Lowest role |
| --- | --- |
| View the organization, its application list, and team list | Unprivileged |
| View repositories, stacks, and servers | Developer |
| Create and manage local-environment servers | Developer |
| View integrations and organization task history | Team leader |
| Add or update shared, development, staging, production, and public servers | Team leader |
| Create applications | Administrator |
| Delete non-local servers | Administrator |
| Create, update, or delete repositories, integrations, and custom stacks | Administrator |
| Manage team membership and organization settings | Administrator |
| View or update billing, payment methods, subscriptions, and invoices | Administrator |
| View member 2FA status | Administrator |
| Require 2FA for the organization | Owner |
| Delete the organization | Owner |

An unprivileged member can see that applications exist in the organization but
cannot open an application's details unless an application-specific role grants
that access.

## Application permissions

| Action | Lowest effective role |
| --- | --- |
| View an application and its development instances | Developer |
| Create, update, deploy, or delete a development instance | Developer |
| View and manage staging or production instances | Team leader |
| Change application settings | Team leader |
| View application and instance task history | Team leader |
| Reveal a protected platform-generated value on an instance the member can update | Same role required to update that instance |
| Deploy a previous CI build or change instance build-retention settings | Same role required to update that instance |
| Delete a staging or production instance | Administrator |
| Delete an application | Administrator |

Actions are also subject to resource state. For example, an operation can be
unavailable while an application, instance, or server is already being updated
or deleted.

## Organization and application roles

You can assign a role at the organization level and a different role for an
individual application. Wodby uses the more privileged of the two roles for
that application. An application role can therefore grant additional access,
but it cannot reduce access inherited from the organization.

When an organization role becomes equal to or more privileged than an existing
application role, Wodby may remove the redundant application membership. The
user keeps the same or greater effective access through the organization.

## Support access

The `Support` role is system-managed and cannot be assigned by organization
owners. It has specific read access needed to handle support cases, does not
inherit the normal role hierarchy, and does not receive ordinary write
permissions.

See [Organizations and membership](organizations.md) for owner, payer, and
last-membership safeguards.
