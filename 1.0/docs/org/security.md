# Organization security

The **Security** tab under **Organization** lets organization owners require two-factor authentication (2FA) for every active member. Only owners can manage this policy, and they must first enable 2FA on their own account.

## Require 2FA for an organization

Organization owners can require every active member to use account-level 2FA:

1. [Enable 2FA for your own account](../user/security.md#enable-two-factor-authentication) under **Account > Security**.
2. Open **Organization > Security**.
3. Select **Require two-factor authentication**.
4. Enter your current password and an authenticator or recovery code.
5. Select **Save security policy**.

## Effects on members

The policy takes effect immediately. It does not remove members, invalidate
their passwords, or end their authenticated session. An active member who has
not enabled 2FA is kept on **Account > Security** after signing in and cannot
continue into the organization until setup is complete. Access is restored as
soon as the member verifies and enables 2FA.

Invited users are not active members until they accept their invitation. After
acceptance, the same requirement applies before they can use the organization.

## Review member status

Owners and administrators can open **Team > List** to see
the 2FA status of each member:

- **Enabled** means the member has account-level 2FA enabled.
- **Not enabled** means the active member must finish setup when enforcement is
  enabled.
- **Not registered** identifies an invitation that has not been accepted yet.

The status is not shown to lower-privileged roles.

## Stop requiring 2FA

To stop enforcing the policy, clear **Require two-factor authentication** and
confirm the change with your password and a second factor. This does not turn
off 2FA for members who already enabled it.
