# Discourse

The Wodby Discourse catalog stack runs [Discourse](https://www.discourse.org/) with PostgreSQL, Redis, and OpenSMTPD.
All four services are required. The current composition is documented in
[`wodby/stack-discourse`](https://github.com/wodby/stack-discourse).

The stack runs Wodby's prebuilt Discourse image, so there's nothing to build and no repository to connect.

## Before you create the app

- Choose a Discourse release line as the Discourse service's version: the monthly release, the default, or the extended
  support release (ESR), which changes less often.
- Set **Administrator email addresses** on the Discourse app service. It is required. Whoever registers an account with
  one of these addresses becomes an administrator. Wodby creates no administrator account.
- Optionally set **Notification email address**. Without it, Discourse derives a sender from the primary hostname. The
  domain of this address should have valid SPF, DKIM, and reverse DNS records.

## Plugins and themes

The plugins bundled with Discourse, such as chat, AI, solved, assign, reactions and voting, are available. Install
themes and theme components from the Discourse administration interface. Other plugins are not supported.

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

## Updates and upgrades

Discourse patch releases arrive as updates of the Discourse service; see
[stack upgrades](../../../apps/stack.md#upgrade). To move to another release line, choose its version on the
[General configuration](../../../apps/services.md#general-configuration) tab and deploy. Back up the app first:
Discourse migrates its database when the new release starts.

Do not update Discourse from its administration interface or install `docker_manager`.

## Data and backups

- The Discourse volume (20 GB by default) holds uploads, backups, and logs.
- PostgreSQL has a 20 GB volume. Redis has a 5 GB volume with persistence on and eviction off. OpenSMTPD has a 1 GB
  queue volume.

Use the Discourse app service backup, **Discourse database and uploads**, for one archive that contains the database and
local uploads. It is Discourse's own backup format. Restore an archive into a disposable app from time to time to verify
recovery. See [Backups](../../../apps/backups.md).

## Apps created before the prebuilt image

Earlier versions of the Discourse stack built Discourse from a repository. Apps created from them keep building from
their repository, because a new major version of a service is never applied automatically. To move to the prebuilt
image, create a new app from the Discourse stack, with the same or a newer Discourse release, and restore a Discourse
backup of the old app into it from **Admin > Backups** in Discourse.

## Limits

- Discourse runs as one replica. It is not scalable.
- The Discourse container requests 0.5 CPU and 2 GiB of memory, with limits of 2 CPU and 4 GiB.
