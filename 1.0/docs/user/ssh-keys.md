# SSH keys

Manage your public SSH keys under `Account > SSH Keys` in the dashboard. Wodby adds these keys to the SSHd container of each instance you can access, when the stack provides one.

## Add a key

1. Open `Account > SSH Keys > Add a new key`.
2. Enter a **Name** that helps you identify the key.
3. Paste your public key into **Value**. Keep the private key on your own device.
4. Click **Submit** and wait for the task to finish. After creation, the dashboard returns to the key list.

## Supported key formats

Wodby supports the following OpenSSH public key types:

* Ed25519 (`ssh-ed25519`) — recommended
* ECDSA with the NIST P-256, P-384, or P-521 curves (`ecdsa-sha2-nistp256`, `ecdsa-sha2-nistp384`, or `ecdsa-sha2-nistp521`)
* RSA (`ssh-rsa`) with a minimum key size of 2048 bits

Paste one public key in OpenSSH format. An optional comment after the key is accepted. Authorized-keys options, DSA keys, hardware-backed FIDO/security-key (`sk-*`) keys, OpenSSH certificates, and post-quantum key types are not supported.

## Review and delete keys

Open `Account > SSH Keys > List` to see each key's name, fingerprint, and status. To remove a key you no longer use, click its delete action and confirm.

## Connect to an instance

Find the SSH command under `Instance > Stack > SSHd` and run it with the matching private key available on your device. Adding a public key does not grant access to instances outside your existing permissions.

See [Accessing containers](../infrastructure/containers.md#accessing-containers) for other ways to access containers.
