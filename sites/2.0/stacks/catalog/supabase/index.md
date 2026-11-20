Source: https://wodby.com/docs/2.0/stacks/catalog/supabase/

# Supabase stack guide

The Supabase stack runs one self-hosted Supabase project per app environment, with a dedicated PostgreSQL database and
the Auth, REST, Realtime, Storage and Studio components. The
[stack source](https://github.com/wodby/stack-supabase) defines its current services and defaults.

## Create an environment

Set these on the Supabase service:

- **Email sender address** and an [SMTP integration](https://wodby.com/docs/2.0/providers/smtp/), both required. Supabase uses them for
  confirmation and recovery emails.
- **Application site URL**, which is where users land after email links and sign-in. Set it to your application's URL.
  If you leave it empty, the public Supabase URL is used, which opens Studio and asks for its password.
- **Additional allowed redirect URLs**, for any other redirect target, such as a custom domain of your application.

**Exposed database schemas** lists the schemas the API can reach. Keep the default unless your application uses a custom
schema.

## Connect your application

Wodby routes HTTPS to the Supabase gateway, and the public Supabase URL follows the service's primary route. Find the
generated keys on the Supabase app service's **Configuration > Tokens** tab:

- `publishable_key` is for client applications, together with the public URL.
- `secret_key` is for trusted server code only. It bypasses row level security and must not reach a browser build.

Sign in to Studio at the public URL with user name `supabase` and the `dashboard_password` token.

Don't generate Supabase keys by hand or copy them from another project. Data encrypted with the service's signing and
encryption tokens can't be read after those tokens change.

## Social sign-in

To let users sign in with GitHub, Google or another provider, register an OAuth application with the provider and
give Supabase Auth its credentials:

1. In the provider's developer settings, create an OAuth application. Set its callback URL to the public Supabase URL
   followed by `/auth/v1/callback`, for example `https://supabase.example.com/auth/v1/callback`, and create a client
   secret.
2. On the Supabase app service, add these [environment variables](https://wodby.com/docs/2.0/apps/environment-variables/), each
   scoped to the `auth` workload and the `auth` container. Replace `GITHUB` with the provider's name, such as `GOOGLE`
   or `GITLAB`.

| Variable | Value |
| --- | --- |
| `GOTRUE_EXTERNAL_GITHUB_ENABLED` | `true` |
| `GOTRUE_EXTERNAL_GITHUB_CLIENT_ID` | the application's client ID |
| `GOTRUE_EXTERNAL_GITHUB_SECRET` | the client secret, marked as secret |
| `GOTRUE_EXTERNAL_GITHUB_REDIRECT_URI` | the callback URL from step 1 |

1. Deploy the app service. The provider then appears as enabled at `/auth/v1/settings` on the public Supabase URL.

In your application, start the sign-in with the Supabase client, for example
`supabase.auth.signInWithOAuth({ provider: 'github' })`. After sign-in, users return to the **Application site URL**,
or to a `redirectTo` address that matches the site URL or an **Additional allowed redirect URL**.

Supabase needs the user's email address. For a GitHub App, set the **Email addresses** account permission to
read-only; a GitHub OAuth App has access by default. Without it, sign-in fails and the user returns to the site URL
with an error in the address. GitLab and Keycloak also need `GOTRUE_EXTERNAL_<PROVIDER>_URL` for a self-hosted
instance. The full list of providers and settings is in the
[Supabase Auth documentation](https://github.com/supabase/auth#external-authentication-providers).

## Database

The database is always `postgres`. Its port is private and gets no public route. Manage tables and policies with
Supabase migrations rather than adding databases or reserved roles. The database password and JWT secret belong to the
Supabase PostgreSQL service, so change them there and never on the Supabase service alone.

## Storage

By default, Storage keeps objects on a persistent volume. To use S3, connect the optional S3 integration, which needs an
access key, a secret key and a region. Set **S3 bucket** to a bucket that already exists, and **S3 endpoint URL** for
storage other than AWS. Wodby doesn't back up an S3 bucket.

## Backups and restore

A consistent recovery point needs all of these together, taken with application writers stopped:

- the database backup, which contains secrets
- the stored objects: the `objects` backup, or your S3 bucket
- the Supabase service's tokens

The database backup doesn't include storage objects or the Supabase service's tokens. The `snippets` backup holds Studio
snippets.

The database [import](https://wodby.com/docs/2.0/apps/imports/) accepts only a `.tar.gz` or `.tgz` backup made by this service with the
same Supabase bundle. An ordinary SQL dump isn't accepted. It restores into a new, empty data volume before the database
accepts connections. If an initialization or import fails, the database won't start normally; run a new import on a
fresh volume.

To restore files, run the Supabase service's `objects` [import](https://wodby.com/docs/2.0/apps/imports/) with the `objects` backup
taken at the same point as the database backup. It replaces everything on the Storage volume with the backup's content,
so files added after that backup are removed. Restore the database and the objects together: the database holds the
file records, so a file without its record isn't visible, and a record without its file fails to download. The
`snippets` import restores Studio snippets the same way. Objects in an S3 bucket are restored outside Wodby.

## Limits

Components run as single replicas. Edge Functions, connection pooling, analytics and high-availability PostgreSQL aren't
included. A rollback doesn't undo database migrations.
