# Mattermost

The Wodby Mattermost catalog stack runs Mattermost Team Edition with PostgreSQL and an optional OpenSMTPD service. The
current composition is documented in [`wodby/stack-mattermost`](https://github.com/wodby/stack-mattermost).

## Before you create the app

- The stack is for simple, single-replica installations. The Mattermost service is fixed to one replica.
- Mattermost must run on a `linux/amd64` node.
- Mattermost Calls is disabled. Calls on Kubernetes needs a separately managed RTCD service and direct TCP and UDP media
  routing.

## First sign-in

Wodby creates no account. Open the app's main route and create the first system administrator in the browser.

## Mail delivery

The OpenSMTPD service is optional. While the Mattermost app service is linked to it, Mattermost receives its SMTP
settings from the link. Attach an [SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production
delivery. See the [OpenSMTPD guide](../opensmtpd/index.md).

## Change configuration

Mattermost reads `MM_<SECTION>_<SETTING>` environment variables. They take precedence over `config.json`, and a setting
given by a variable cannot be changed in the System Console.

Wodby sets variables for the site URL, the database, mail (while the link exists), the maximum file size, and logging.
Change them as environment variables on the app service and deploy it. Change other settings in the System Console. They
are saved to `config.json` on the volume. See [Environment variables](../../../apps/environment-variables.md).

Mattermost limits files to 100 MB, and the route accepts request bodies up to 128 MiB. If you raise the Mattermost file
limit, raise the route's request body size too.

## Data and backups

The Mattermost volume (20 GB by default) holds uploaded files, `config.json`, server plugins, and web application
plugins. Everything else is in PostgreSQL, which has its own 20 GB volume.

Back up the database and the Mattermost volume together as one recovery set. The Mattermost service has no backup or
import operation in Wodby. The PostgreSQL service does. See [Backups](../../../apps/backups.md).
