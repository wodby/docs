---
description: Deploy Mautic with your own plugins and themes on Wodby with the buildable Mautic stack, which builds the Mautic Composer project in your Git repository.
---

# Mautic (buildable)

The buildable Mautic stack runs [Mautic](https://www.mautic.org/) built from your Git repository: a Mautic Composer
project whose lock file pins Mautic and the plugins and themes you install with Composer. The stack has the same
services as the [Mautic stack](../mautic/index.md): MariaDB, shared NFS storage for Mautic's files, cron and queue
workers, and OpenSMTPD. Its composition is documented in
[`wodby/stack-mautic-buildable`](https://github.com/wodby/stack-mautic-buildable).

Everything in the [Mautic guide](../mautic/index.md) applies, from the administrator settings to workers, mail and
backups. This page covers what differs.

## Repository

Start the repository from the [Mautic boilerplate](https://github.com/wodby/mautic-boilerplate), Mautic's recommended
Composer project with a `composer.lock`, and connect it when you create the app.

- Add plugins and themes with Composer, for example `composer require mautic/helloworld-bundle`.
- Or commit a plugin or theme of your own under `docroot/plugins/` or `docroot/themes/`, and re-include it in
  `.gitignore`, such as `!/docroot/plugins/MyPluginBundle/`.

Don't commit `config/local.php`: Mautic writes its settings there, and Wodby keeps that file on the shared files
volume.

## Build

The build runs `composer install`, which installs Mautic and your packages, runs `npm` and generates Mautic's assets,
then adds Wodby's settings on top of Wodby's PHP image for Mautic.

The build fails when `composer.json` or `composer.lock` is missing, or when the repository has a `config/local.php`.

## Plugins and updates

After every deployment Wodby runs Mautic's database migrations and reloads its plugins, so new plugins are installed
and updated ones are upgraded. The cron and queue workers run the same build.

To update Mautic, run `composer update "mautic/*" --with-all-dependencies`, commit `composer.lock` and deploy. You
decide when to update, so watch [Mautic's releases](https://github.com/mautic/mautic/releases) for security fixes.

To have Wodby keep Mautic up to date instead, use the [Mautic stack](../mautic/index.md).
