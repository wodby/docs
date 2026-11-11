---
description: Deploy n8n, the workflow automation tool, on Wodby with the n8n catalog stack, which runs the Community Edition with PostgreSQL and optional OpenSMTPD.
---

# n8n

The Wodby n8n catalog stack runs [n8n](https://n8n.io/), the workflow automation tool, from the official Community
Edition image, with PostgreSQL and an optional OpenSMTPD service for mail. The current composition is documented in
[`wodby/stack-n8n`](https://github.com/wodby/stack-n8n).

## Owner account

Set the owner account in the n8n service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Owner email | none, required | The email address the owner signs in with |
| Owner password | none, required | The owner's password, at least 8 characters |
| Timezone | `UTC` | The default timezone of schedules and date functions, such as `Europe/Berlin` |

n8n applies the owner's email and password on every start, so its setup page is never shown and nobody else can claim a
new installation. Open the app's domain and sign in with these credentials.

You can't change the owner's email or password in n8n. Change them in the service's **Configuration > Settings** and
deploy the n8n service. The owner is then signed out and signs in with the new values. If the password is shorter than 8
characters, n8n does not start, and the n8n service log says why. See
[Settings tab](../../../apps/services.md#settings-tab).

To let other people in, invite them in n8n. Invitations are sent by email; see [Mail](#mail).

## Webhooks and the editor URL

n8n builds webhook URLs and editor links from the n8n service's primary domain. After you add a domain or change the
primary domain, deploy the n8n service so that n8n shows webhook URLs with the new domain. If you remove the old
domain, update the webhook URLs in the systems that call them. See [Domains](../../../apps/endpoints.md#domains).

The route has no request timeout, so a webhook can wait for its workflow to finish before it answers. Do not set the
route's request body size: it makes the route hold each request in memory until it is complete, and the editor's live
connection stops working. See [HTTP settings](../../../apps/endpoints.md#http-settings).

## Code nodes

JavaScript and Python Code nodes run in a separate task runner container next to n8n, at the same version as n8n. A Code
node may run for up to 5 minutes.

Which modules Code nodes may import is set in the runner image. By default, Python Code nodes can't import
standard-library modules, and JavaScript Code nodes can use `crypto` and `moment`. Environment variables you add to the
n8n service do not reach the runner.

The runner has its own CPU and memory, up to 1 CPU and 1 GB by default. Raise them in **Runtime > Resources** if Code
nodes process large data. See [Resources tab](../../../apps/services.md#resources-tab).

## Mail

n8n sends user invitations and password resets by email. The owner account doesn't need mail, so the OpenSMTPD service
is disabled by default. Enable it to send n8n's mail, and attach an
[SMTP provider integration](../../../providers/smtp.md) to it for production delivery. See the
[OpenSMTPD guide](../opensmtpd/index.md).

While n8n is linked to OpenSMTPD, mail is sent from `noreply@` the n8n service's primary hostname. If your provider
accepts only other senders, set the `N8N_SMTP_SENDER` environment variable on the n8n service, for example
`n8n <automation@example.com>`, and deploy it. See [Environment variables](../../../apps/environment-variables.md).

## Data and backups

- PostgreSQL (10 GB by default) holds workflows, credentials, executions, users, and settings.
- The n8n volume (10 GB by default) holds community nodes, binary data, and n8n's own files.

n8n encrypts saved credentials with a key Wodby generates for the n8n service, the `encryption_key` token in
**Configuration > Tokens**. Keep it and keep a copy. If the key changes, n8n can no longer read saved credentials. A
database restored into another environment needs the same key. See [Tokens](../../../apps/tokens.md).

Back up the database and the n8n volume together as one recovery set. The n8n service has no backup or import operation
in Wodby. The PostgreSQL service does. See [Backups](../../../apps/backups.md) and [Imports](../../../apps/imports.md).

## Upgrades

n8n migrates its database when a newer version starts, for example after a stack upgrade, and an older version can't
use the migrated database. Back up the PostgreSQL database before you upgrade.

## Limits

- The n8n service is fixed to one replica. n8n's queue mode, with Redis and separate worker processes, is not set up by
  this stack.
- n8n is unavailable for a short time while its service is deployed.
- n8n's [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) allows use for your own internal
  business purposes or for non-commercial or personal use. Check it before you offer n8n to others.
