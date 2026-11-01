# Discourse

The Wodby Discourse catalog stack builds Discourse from source and runs it with PostgreSQL, Redis, and OpenSMTPD. All
four services are required. The current composition is documented in
[`wodby/stack-discourse`](https://github.com/wodby/stack-discourse).

## Before you create the app

- Choose a build source: the Discourse stable or ESR boilerplate, a clone of one in your own repository, or a compatible
  Discourse fork. Wodby CI builds it. See [Application Builds](../../../apps/builds.md).
- Set **Administrator email addresses** on the Discourse app service. It is required. Whoever registers an account with
  one of these addresses becomes an administrator. Wodby creates no administrator account.
- Optionally set **Notification email address**. Without it, Discourse derives a sender from the primary hostname. The
  domain of this address should have valid SPF, DKIM, and reverse DNS records.

A source whose frontend differs from the Discourse release, such as a fork with frontend changes, builds its own
frontend. That takes considerably longer.

## Mail delivery

Discourse sends mail through the stack's OpenSMTPD service, and account and administration workflows depend on it.
Attach an [SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for reliable delivery. Without a relay,
mail leaves directly from the cluster address, and recipient providers often reject it. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Change configuration

The two settings above and the links supply the database, Redis, and mail values. Do not set those values elsewhere.

Add other upstream `DISCOURSE_*` settings through the **Additional environment variables** integration. A change
applies with the next deployment of the app service. A site setting that has a variable of the same name takes its value
from the variable and cannot be changed in the Discourse administration interface.

On every start, Discourse applies database migrations and rebuilds theme and CSS assets. The health endpoint is
`/srv/status`.

## Data and backups

- The Discourse volume (20 GB by default) holds uploads, backups, and logs.
- PostgreSQL has a 20 GB volume. Redis has a 5 GB volume with persistence on and eviction off. OpenSMTPD has a 1 GB
  queue volume.

Use the Discourse app service backup, **Discourse database and uploads**, for one archive that contains the database and
local uploads. Restore an archive into a disposable app from time to time to verify recovery. See
[Backups](../../../apps/backups.md).

## Limits

- Discourse runs as one replica. It is not scalable.
- The Discourse container requests 0.5 CPU and 2 GiB of memory, with limits of 2 CPU and 4 GiB.
- Upgrade by building a newer supported Discourse Git ref. Do not update Discourse from its administration interface or
  install `docker_manager`.
