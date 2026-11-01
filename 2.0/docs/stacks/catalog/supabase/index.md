# Supabase

The Supabase stack runs one self-hosted Supabase project per app environment, with a dedicated PostgreSQL database and
the Auth, REST, Realtime, Storage and Studio components. The
[stack source](https://github.com/wodby/stack-supabase) defines its current services and defaults.

## Create an environment

Set these on the Supabase service:

- **Email sender address** and an [SMTP integration](../../../providers/smtp.md), both required. Supabase uses them for
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

The database [import](../../../apps/imports.md) accepts only a `.tar.gz` or `.tgz` backup made by this service with the
same Supabase bundle. An ordinary SQL dump isn't accepted. It restores into a new, empty data volume before the database
accepts connections. If an initialization or import fails, the database won't start normally; run a new import on a
fresh volume.

## Limits

Components run as single replicas. Edge Functions, connection pooling, analytics and high-availability PostgreSQL aren't
included. A rollback doesn't undo database migrations.
