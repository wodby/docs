# Account security

Wodby 1 supports two-factor authentication (2FA) for individual user accounts.
When 2FA is enabled, signing in requires both your password and a time-based
code from a compatible TOTP authenticator app. You can enable it voluntarily,
and an organization owner can require it for every active member of an
organization.

## Enable two-factor authentication

1. In the Wodby dashboard, open **Account > Security**.
2. Enter your current password and select **Enable two-factor authentication**.
3. Scan the QR code with your authenticator app. If you cannot scan it, enter
   the displayed setup key manually.
4. Enter the six-digit code from the authenticator and select
   **Verify and enable**.
5. Download or copy the ten recovery codes and store them somewhere secure.

!!! warning
    The QR code and setup key contain the secret used to generate your
    authentication codes. Do not share them or store screenshots in a shared
    location.

Two-factor authentication is not enabled until the authenticator code has been
verified. If the setup expires before you finish, start the process again from
**Account > Security**.

## Sign in with 2FA

Enter your email address and password as usual. Wodby then asks for either:

- the current six-digit code from your authenticator app; or
- an unused recovery code.

The second-factor challenge expires after five minutes. If it expires, return
to the first login step and enter your email address and password again.

Links that would otherwise sign an existing user in automatically, including
organization invitation links, do not bypass 2FA. Wodby redirects the user to
the dashboard login flow to complete authentication.

If a valid authenticator code is rejected, make sure automatic date and time
are enabled on the device running your authenticator app, then try the newest
code.

## Recovery codes

Each recovery code can be used once in place of an authenticator code during
login. The Security page shows how many unused codes remain, but it cannot show
their values again after initial generation.

To replace your recovery codes:

1. Open **Account > Security** and select **Generate new recovery codes**.
2. Enter your current password and a code from your authenticator app.
3. Save the newly generated codes.

Generating new codes immediately invalidates every previous recovery code.

## Require 2FA for an organization

Organization owners can require every active member to use account-level 2FA:

1. Enable 2FA for your own account under **Account > Security**.
2. Open **Organization > Settings > Security**.
3. Select **Require two-factor authentication**.
4. Enter your current password and an authenticator or recovery code.
5. Select **Save security policy**.

The policy takes effect immediately. It does not remove members, invalidate
their passwords, or end their authenticated session. An active member who has
not enabled 2FA is kept on **Account > Security** after signing in and cannot
continue into the organization until setup is complete. Access is restored as
soon as the member verifies and enables 2FA.

Invited users are not active members until they accept their invitation. After
acceptance, the same requirement applies before they can use the organization.

Owners and administrators can open **Organization > Settings > Team** to see
the 2FA status of each member:

- **Enabled** means the member has account-level 2FA enabled.
- **Not enabled** means the active member must finish setup when enforcement is
  enabled.
- **Not registered** identifies an invitation that has not been accepted yet.

The status is not shown to lower-privileged roles.

To stop enforcing the policy, clear **Require two-factor authentication** and
confirm the change with your password and a second factor. This does not turn
off 2FA for members who already enabled it.

## Disable two-factor authentication

Open **Account > Security**, select **Disable two-factor authentication**, and
enter your current password plus either an authenticator code or an unused
recovery code. Future logins will require only your password.

You cannot disable account-level 2FA while you are an active member of any
organization that requires it. An organization owner must first disable that
policy or remove your active membership.

## Lost authenticator access

If you are already signed in, disable 2FA with your current password and an
unused recovery code, then enable it again with the new authenticator.

If you are signed out, you need two unused recovery codes: one to sign in and a
different one to disable 2FA. You can then enable 2FA again and save the new set
of recovery codes. A recovery code is consumed as soon as it is used, so the
same code cannot complete both steps.

Resetting your password does not disable 2FA.

If you do not have enough unused recovery codes, contact
[Wodby support](support.md). Be prepared to verify that you own the account.
