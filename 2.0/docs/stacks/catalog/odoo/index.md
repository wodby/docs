---
description: Deploy Odoo Community Edition 20, 19 or 18 on Wodby with the Odoo catalog stack, which runs it with Nginx, PostgreSQL and shared NFS storage.
---

# Odoo

The Wodby Odoo catalog stack runs [Odoo](https://www.odoo.com/) Community Edition 20, 19 or 18 with Nginx, PostgreSQL,
shared NFS storage for Odoo's files, and an optional OpenSMTPD service for mail. The current composition is documented
in [`wodby/stack-odoo`](https://github.com/wodby/stack-odoo).

The stack needs no repository: Odoo and every Community app come with the service's image. Install apps from Odoo's
**Apps** menu, or list them in the **Apps to install** setting when you create the app.

## Your own modules

To add your own or community modules, use the
[buildable Odoo stack](https://github.com/wodby/stack-odoo-buildable) instead. You keep the modules and their Python
packages in a Git repository started from the [Odoo boilerplate](https://github.com/wodby/odoo-boilerplate), and Wodby
builds Odoo with them on every push. Installed modules whose files change are updated when you deploy; new modules
appear in the **Apps** menu.

## Administrator account

Odoo is installed during the app's first deployment. Its database manager is turned off, so databases can't be created,
copied or dropped from the web. Set up the installation in the Odoo service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Admin password | none, required | The administrator's password |
| Admin login | `admin` | The administrator's login |
| Admin email | empty | The administrator's email address |
| Language | English | A language to install and give the administrator, such as `fr_FR` |
| Apps to install | none | Apps installed with Odoo, such as `crm,sale_management` |

- The company starts with the app's title as its name. Change it in Odoo's settings.
- No demo data is loaded.

These settings are only used when Odoo is installed. To change the administrator later, use Odoo.

If the first deployment can't install Odoo, for example because the admin password is missing, the deployment's
post-deploy step fails with the reason. Fix it and deploy again.

## Updates

Odoo updates arrive with new revisions of the service's image. After each deployment, Odoo updates the installed apps
whose version went up. To update every installed app, run the **Update all modules** action of the Odoo service.

To add your own or community modules, build an image `FROM wodby/odoo` with the modules in `/usr/src/app`, and use it
from a [custom service](../../../services/create.md) based on the Odoo service.

## Workers and live updates

Each Odoo replica runs 2 worker processes and 1 process for scheduled actions by default; change the **Workers** and
**Scheduled action workers** settings to match the service's memory. A separate process serves live updates such as
chat and notifications, and the Nginx service sends them to it. Keep at least 1 worker.

## Mail

Enable the OpenSMTPD service to send Odoo's mail through it, and attach an
[SMTP provider integration](../../../providers/smtp.md) for production delivery; see the
[OpenSMTPD guide](../opensmtpd/index.md). You can also set up an outgoing mail server in Odoo's settings.

## Data and backups

- The `filestore` volume holds uploaded files and sessions. Every Odoo replica shares it through the NFS storage service.
- The PostgreSQL database holds everything else.

Back up both the database and the `filestore` volume; see [Application Backups](../../../apps/backups.md). Back up the
app before you move to a new major Odoo version: Odoo doesn't migrate a database between major versions by itself.

## Limits

- Odoo Community Edition only. Enterprise modules need a custom image, like your own modules.
- One database per app environment.
- Uploads are limited to 128 MB.
