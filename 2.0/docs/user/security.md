# Security

The `Security` section in user settings covers password management, two-factor authentication, and recovery codes.

## Password

You can change your password from `User settings > Security`.

Sensitive security actions are protected by password confirmation when required.

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
