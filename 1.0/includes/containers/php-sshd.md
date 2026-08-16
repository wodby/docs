A duplicate of the PHP container runs an SSH daemon instead of FPM. You can find access information on `[Instance] > Stack > SSH`.

Public SSH keys from your Wodby profile are added automatically for every user who has access to the instance.

Wodby supports the following OpenSSH public key types:

* Ed25519 (`ssh-ed25519`) — recommended
* ECDSA with the NIST P-256, P-384, or P-521 curves (`ecdsa-sha2-nistp256`, `ecdsa-sha2-nistp384`, or `ecdsa-sha2-nistp521`)
* RSA (`ssh-rsa`) with a minimum key size of 2048 bits

Paste one public key in OpenSSH format. An optional comment after the key is accepted. Authorized-keys options, DSA keys, hardware-backed FIDO/security-key (`sk-*`) keys, OpenSSH certificates, and post-quantum key types are not supported.
