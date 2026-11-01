# Chatwoot

The Wodby Chatwoot catalog stack runs Chatwoot with a Sidekiq worker, PostgreSQL with pgvector, Redis, shared
attachment storage, and an optional OpenSMTPD service. The current composition is documented in
[`wodby/stack-chatwoot`](https://github.com/wodby/stack-chatwoot).

## Settings to review when creating the app

Set these on the Chatwoot app service:

- **Account signup**: `false` by default, which disables public signup. `api_only` allows signup through the API only.
- **Mailer sender**: the address Chatwoot uses for outbound email. Use an address your mail relay accepts.
- **Force SSL**, **Default locale**, **Log level**, **Rails threads**, and **Sidekiq concurrency**.

Wodby generates the application secret and the three Active Record encryption keys when the app is created. They are
tokens on the app service's **Configuration > Tokens** tab.

On start, the web container prepares the database. Later deployments apply new migrations the same way.

## Mail delivery

OpenSMTPD is optional, but SMTP is recommended for password resets and notifications. If you keep it, attach an
[SMTP provider integration](../../../providers/smtp.md) for production delivery. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Attachments and object storage

Attachments are stored on the shared `/app/storage` volume, which the **Shared attachment storage** service provides.

To use S3, S3-compatible storage, Google Cloud Storage, or Azure Storage instead, attach the **Additional Chatwoot
environment variables** integration. Add the variables that Chatwoot requires for the storage provider, and override
`ACTIVE_STORAGE_SERVICE`.

## Data and backups

- PostgreSQL stores Chatwoot's relational data.
- Redis stores queue data with persistence on and eviction off.
- The shared attachment storage service stores local attachments.

Back up both the PostgreSQL database and the shared attachment storage service to keep a complete installation. See
[Backups](../../../apps/backups.md) and [Imports](../../../apps/imports.md).
