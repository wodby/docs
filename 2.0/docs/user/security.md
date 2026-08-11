# Security

The `Security` section in user settings covers password management, two-factor authentication, and recovery codes.

## Password

You can change your password from `User settings > Security`.

Sensitive security actions are protected by password confirmation when required.

## Secret reveal confirmation

Displaying a stored app or database credential requires an interactive user session and the appropriate
[secret reveal permission](../access-control.md#secret-reveal-permissions).

When you click a reveal action, Wodby opens a dialog and checks whether you signed in or completed another confirmation
during the last five minutes. If additional confirmation is needed, the dialog uses an authentication method available
for your account:

- accounts with a Wodby password confirm their current password
- passwordless accounts with 2FA enter an authenticator or recovery code
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

1. confirm your password
2. save the generated recovery codes
3. scan the QR code or enter the secret manually in your authenticator app
4. enter the 6-digit verification code

Recovery codes are shown before final verification so you can store them safely.

### Disabling 2FA

Disabling 2FA also requires password confirmation.

## Recovery codes

Recovery codes are managed from the same security area.

- viewing recovery codes requires password confirmation
- regenerating recovery codes requires password confirmation
- when you regenerate them, replace your previously stored set

## Related pages

- [User settings](index.md)
- [API keys](api-keys.md)
