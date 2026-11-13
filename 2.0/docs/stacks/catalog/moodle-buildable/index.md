---
description: Deploy Moodle with your own plugins and themes on Wodby with the buildable Moodle stack, which builds the Moodle release you pin in Git with your plugins.
---

# Moodle (buildable)

The buildable Moodle stack runs [Moodle](https://moodle.org/) built from your Git repository: the repository pins the
Moodle release and holds your own plugins and themes. The stack has the same services as the
[Moodle stack](../moodle/index.md): Nginx, MariaDB, shared NFS storage for Moodle's data, a cron worker, OpenSMTPD and
optional Valkey. Its composition is documented in
[`wodby/stack-moodle-buildable`](https://github.com/wodby/stack-moodle-buildable).

Everything in the [Moodle guide](../moodle/index.md) applies, from the administrator settings to cron, sessions and
backups. This page covers what differs.

## Repository

Start the repository from the [Moodle boilerplate](https://github.com/wodby/moodle-boilerplate) and connect it when you
create the app.

| Path | Purpose |
| --- | --- |
| `.moodle-version` | The Moodle release to run, such as `5.3.1`. Required. |
| `public/` | Your plugins and themes, at their place in Moodle's `public/` tree, such as `public/local/myplugin` |
| `.wodby/pipeline.yml` | The pipeline, which puts Moodle together before building the images |

Moodle 5.1 and later 5.x releases are supported.

## Build

Before building the images, the pipeline runs `moodle-install-release`. It downloads the release with its Composer
packages and adds your `public/` files and Wodby's settings file. The Moodle and Nginx images are then built from the
same code, so Nginx serves your plugins' and themes' files.

The build fails when `.moodle-version` is missing, or when a file in `public/` is already part of Moodle: your plugins
are added next to Moodle's code and never replace it.

## Plugins

Each deployment installs or upgrades Moodle, installs plugins that are new in the repository and upgrades those whose
version went up. The cron worker runs the same build, so your plugins' scheduled tasks run too.

Uninstall a plugin in Moodle's administration before you remove it from the repository. Plugins can't be installed
from Moodle's web interface, because the code is part of the image.

## Updates

Moodle's version changes only when you change `.moodle-version` and deploy; the deployment upgrades the database.
Updates of the service bring PHP and Wodby's own changes, not a new Moodle. You decide when to upgrade, so watch
[Moodle's releases](https://moodledev.io/general/releases) for security fixes.

To have Wodby keep Moodle up to date instead, use the [Moodle stack](../moodle/index.md).
