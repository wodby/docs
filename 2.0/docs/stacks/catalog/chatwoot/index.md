# Chatwoot

The Wodby Chatwoot catalog stack runs Chatwoot with a Sidekiq worker, PostgreSQL with pgvector, Redis, shared
attachment storage, and an optional OpenSMTPD service. The current composition is documented in
[`wodby/stack-chatwoot`](https://github.com/wodby/stack-chatwoot).

## Sign in as the first administrator

Set **Admin email** on the Chatwoot app service when you create the app. Replace the `admin@example.com` placeholder
with your own address, because Chatwoot sends password resets to it.

At the end of the first deployment, Wodby creates a super admin and a first Chatwoot account named `Chatwoot`, and
closes Chatwoot's onboarding page. No mail is needed.

1. Open the Chatwoot app service's **Configuration > Tokens** tab and reveal `admin_password`. See
   [Tokens](../../../apps/tokens.md).
2. Open the app's main domain and sign in with **Admin email** and that password.
3. Change the password in your profile settings, and rename the account under **Settings > Account Settings**.

The token and **Admin email** are used only while no super admin exists. Changing them later does not change an existing
administrator, and neither does a later deployment. To change the administrator's address, edit the user in the Super
Admin console at `/super_admin`. This is also how you replace the placeholder if you kept it.

## Upgrade an existing environment

When you upgrade the stack, **Admin email** is added with the `admin@example.com` placeholder and `admin_password` is
generated.

- If the environment already has a super admin, nothing changes. Keep signing in with your existing account.
- If nobody finished the onboarding page, the deployment after the upgrade creates the administrator and closes the page.
  Sign in as described above, then replace the placeholder address in the Super Admin console.

## Settings to review when creating the app

Set these on the Chatwoot app service:

- **Admin email**: the first administrator's sign-in address. Required.
- **Account signup**: `false` by default, which disables public signup. `api_only` allows signup through the API only.
  The first administrator does not depend on this setting.
- **Mailer sender**: the address Chatwoot uses for outbound email. Use an address your mail relay accepts.
- **Force SSL**, **Default locale**, **Log level**, **Rails threads**, and **Sidekiq concurrency**.

Wodby generates the first administrator's password, the application secret, and the three Active Record encryption keys
when the app is created. They are tokens on the app service's **Configuration > Tokens** tab.

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
