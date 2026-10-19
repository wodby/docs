# Account

Your user account can belong to multiple [organizations](../org.md). Each
organization controls access to its own resources through [roles](../access-control.md).

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
[two-factor authentication policy](security.md#require-2fa-for-an-organization).
