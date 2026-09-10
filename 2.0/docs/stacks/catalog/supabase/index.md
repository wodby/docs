# Supabase

The Supabase stack runs one self-hosted Supabase project per app environment, with a dedicated database and the Auth,
REST, Realtime, Storage and Studio components. The [stack source](https://github.com/wodby/stack-supabase) and its service
manifests define the supported component bundle and current defaults.

## Initial setup

Set the application site URL, allowed authentication redirects and sender email address. Connect an SMTP integration
for confirmation and recovery emails. Wodby routes the public Supabase URL to the API gateway. Studio uses username
`supabase` and the generated `dashboard_password` service token.

Client applications use the public URL and the `publishable_key` token. Trusted server applications may use
`secret_key`; it bypasses ordinary user row-level security and must not be included in browser code.

## Storage

The default filesystem backend keeps Storage objects on a persistent volume, shared with image processing in the
same pod. Studio snippets have separate persistence. Optional S3 storage uses an existing bucket and a variable
integration providing `AWS_ACCESS_KEY_ID`, secret `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`. Set the service's bucket
and optional custom endpoint settings before connecting it. Existing filesystem objects are not migrated automatically.

## Backup, restore and copies

Establish a coordinated recovery point with application writers stopped. Preserve database dumps, database encryption
material, all database/application source tokens, and the corresponding stored objects. The filesystem backup does
not include objects stored in an external S3 bucket.

Restore into a fresh environment running the same supported bundle, following the database service's restore guide.
Restore matching source tokens and objects before restarting the services. Copies retain token values; rotate
client-facing credentials deliberately when the copy needs separate access, while preserving encryption keys needed
to read copied data.

## Upgrades and limitations

Upgrade the tested component bundle together. Changing a PostgreSQL major image tag against an existing data directory
is not a supported upgrade procedure. A Helm rollback does not undo database migrations.

The initial stack uses single-replica components. Edge Functions, connection pooling, Supabase analytics, MCP and
high-availability PostgreSQL are not included. Supabase Cloud organization management, branching and managed PITR are
separate capabilities. See the [Supabase self-hosting documentation](https://supabase.com/docs/guides/self-hosting)
for the distinction from the hosted platform.
