---
description: Change your Wodby password, set up two-factor authentication, manage recovery codes, and confirm it is you before revealing secrets.
---

# Security

The `Security` section in user settings covers password management, two-factor authentication, and recovery codes.

## Password

You can change your password from `User settings > Security`.

To change your password, enter your current one. If your account has no password yet, for example because you sign in
with Google or GitHub, setting the first one needs a [recent confirmation](#changes-to-how-you-sign-in).

## Changes to how you sign in

These changes affect who can sign in to your whole account, so Wodby asks you to confirm it's you if you haven't signed
in or confirmed during the last five minutes:

- setting a first password
- enabling or disabling 2FA
- generating new recovery codes
- adding or deleting an email address, or changing your primary email
- unlinking a sign-in identity
- deleting an account that has no password

You confirm in the same way as for a [secret reveal](#secret-reveal-confirmation).

These changes are only available in a signed-in browser session. [API keys](../dev/api-keys.md) and tokens can't make
them, or change a password or delete an account, and get an error instead.

## Secret reveal confirmation

Displaying a stored app or database credential requires an interactive user session and the appropriate
[secret reveal permission](../access-control.md#secret-reveal-permissions).

When you click a reveal action, Wodby opens a dialog and checks whether you signed in or completed another confirmation
during the last five minutes. If additional confirmation is needed, the dialog uses an authentication method available
for your account:

- accounts with 2FA enter an authenticator or recovery code
- other accounts with a Wodby password confirm their current password
- other passwordless accounts receive a six-digit code at their verified primary email address

An email code expires after five minutes, and requests and verification attempts are limited. After confirmation, the
secret is displayed for 30 seconds and is then removed from the dialog. Closing the dialog removes it immediately.

Secret reveal responses are not cached. API-key and token authentication cannot use direct reveal operations.

Copying a value places it on your device's clipboard; Wodby cannot clear that copy automatically. Move long-lived
credentials into an approved secrets manager and rotate any value that may have been exposed.

## Two-factor authentication

Wodby supports two-factor authentication with a one-time password authenticator app.

### Enrolling in 2FA

The enrollment flow is:

1. confirm it's you, if you haven't recently
2. save the generated recovery codes
3. scan the QR code or enter the secret manually in your authenticator app
4. enter the 6-digit verification code

Recovery codes are shown before final verification so you can store them safely.

### Disabling 2FA

Disabling 2FA also requires a [recent confirmation](#changes-to-how-you-sign-in).

## Recovery codes

Recovery codes are managed from the same security area.

- recovery codes are only shown when they are generated
- generating new codes requires a [recent confirmation](#changes-to-how-you-sign-in)
- when you generate new codes, replace your previously stored set

## Related pages

- [User settings](index.md)
- [API keys](api-keys.md)
