# Organizations and membership

An organization owns its applications, servers, repositories, integrations,
stacks, API keys, billing information, and team memberships. Access to those
resources is controlled by each member's organization role and, where
configured, an application-specific role. See [Permissions](roles.md) for the
role hierarchy.

## Manage members

Owners and administrators can invite people and manage active memberships from
`Organization > Settings > Team`. An invitation does not become an active
membership until the invited person accepts it.

The following safeguards apply when changing or removing a membership:

- An organization must always have at least one owner.
- A member cannot be removed if this is their only active organization.
- If the member is the organization's billing payer, another active owner must
  be available to take over billing first.
- An application-specific role can grant more access to one application, but
  it cannot reduce access already granted by the organization role.

When the billing payer is removed, Wodby transfers the billing contact to the
successor owner. The existing subscription, payment source, and invoice history
remain attached to the organization.

## Delete an organization

Only an owner can delete an organization. Before deletion can start, remove or
resolve all of the following:

- applications and their instances;
- connected servers;
- repositories and integrations;
- custom stacks;
- organization-scoped API keys;
- other members and outstanding invitations;
- an active subscription; and
- active organization tasks.

The owner must also belong to another active organization so their account has
a remaining organization context. After the readiness check passes, deletion
runs as a task rather than completing immediately.

!!! warning "Deletion and server data"
    Deleting control-plane resources does not necessarily erase persistent
    application or backup files from a connected server. Review
    [instance deletion](apps/instances.md#deleting-an-instance) and
    [disk cleanup](infrastructure/disk.md#application-and-backup-data) before
    decommissioning the server.

## Delete your account

Open `Account > Delete`, review the consequences, and enter your current
password. Account deletion removes your memberships, API keys, integrations,
authentication tokens, and other account-owned access records.

Organizations for which you are the sole owner are deleted as part of the
account-deletion task. Organizations with another owner remain active and your
membership is removed. If you are the billing payer for an organization that
will remain active, another active owner must be available to inherit billing;
otherwise account deletion is blocked.

Account deletion does not bypass an organization's
[two-factor authentication policy](account-security.md#require-2fa-for-an-organization).
