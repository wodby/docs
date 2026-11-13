---
description: Deploy Matomo with your own plugins on Wodby with the buildable Matomo stack, which builds the Matomo release you pin in Git with your plugins.
---

# Matomo (buildable)

The buildable Matomo stack runs [Matomo](https://matomo.org/) built from your Git repository: the repository pins the
Matomo release and holds your own plugins. The stack has the same services as the [Matomo stack](../matomo/index.md):
MariaDB, shared NFS storage for Matomo's files, and OpenSMTPD for mail. Its composition is documented in
[`wodby/stack-matomo-buildable`](https://github.com/wodby/stack-matomo-buildable).

Everything in the [Matomo guide](../matomo/index.md) applies, from the superuser settings to archiving, mail and
backups. This page covers what differs.

## Repository

Start the repository from the [Matomo boilerplate](https://github.com/wodby/matomo-boilerplate) and connect it when you
create the app.

| Path | Purpose |
| --- | --- |
| `.matomo-version` | The Matomo release to run, such as `5.14.2`. Required. |
| `plugins/` | Your plugins, one directory per plugin, named like the plugin |

Matomo 5 releases are supported. The build downloads the release from Matomo, checks its signature and installs it
with your plugins on Wodby's PHP image for Matomo.

The build fails when `.matomo-version` is missing, when a directory in `plugins/` has no `plugin.json`, or when a
plugin has the name of one of Matomo's own plugins.

## Plugins

On every deployment Wodby installs Matomo or updates its database, activates every plugin from the repository, and
deactivates the plugins you removed from the repository since the last deployment. A plugin from the repository can't
stay deactivated: remove it from the repository instead.

Plugins installed from Matomo's Marketplace work as on the Matomo stack: they are kept on the shared files volume, not
in the repository.

## Updates

Matomo's version changes only when you change `.matomo-version` and deploy; the deployment updates Matomo's database.
Updates of the service bring PHP and Wodby's own changes, not a new Matomo. You decide when to upgrade, so watch
[Matomo's releases](https://matomo.org/changelog/) for security fixes.

To have Wodby keep Matomo up to date instead, use the [Matomo stack](../matomo/index.md).
