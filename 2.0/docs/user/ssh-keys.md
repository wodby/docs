# SSH keys

Manage your SSH public keys from `User settings > SSH keys`.

These keys are propagated to supported SSHD app services that you can modify.

## What happens when you add or remove a key

Wodby adds your SSH keys to SSHD app services with a published port in apps where you have writable access.

Changing your SSH keys triggers redeployment of those SSHD services so the updated authorized keys can be applied.

## Supported key formats

The dashboard accepts the following public key types:

- `ssh-rsa`
- `ssh-ed25519`
- `ecdsa-sha2-nistp256`
- `ecdsa-sha2-nistp384`
- `ecdsa-sha2-nistp521`

## Key details

The key details page shows the key fingerprint and lets you delete the key.

Deleting a key also triggers redeployment of affected SSHD services.

## Related pages

- [User settings](index.md)
- [App services](../apps/services.md)
