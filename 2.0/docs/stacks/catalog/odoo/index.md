# Odoo

The Wodby Odoo catalog stack runs [Odoo](https://www.odoo.com/) Community Edition 20, 19 or 18 with Nginx, PostgreSQL,
shared NFS storage for Odoo's files, and an optional OpenSMTPD service for mail. The current composition is documented
in [`wodby/stack-odoo`](https://github.com/wodby/stack-odoo).

Odoo itself comes with the service's image. Your repository holds only the modules you add: start with the Odoo modules
boilerplate, or connect a repository of your own modules.

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

## Modules

Add your modules to the repository, one directory per module, and deploy. Every directory up to three levels deep that
contains modules is added to Odoo's addons path, so you can also add community repositories, such as OCA ones, as Git
submodules. Python packages your modules need go in `requirements.txt`.

After each deployment, Odoo updates the installed modules whose version went up and the installed modules of your
repository whose files changed. New modules appear in the **Apps** menu; install them from there. To update every
installed module, run the **Update all modules** action of the Odoo service.

Odoo's code is part of the build image, so apps you install from Odoo's Apps menu must be ones the image or your
repository already contains.

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

- Odoo Community Edition only. If you have an Odoo Enterprise subscription, add the Enterprise modules to your
  repository.
- One database per app environment.
- Uploads are limited to 128 MB.
