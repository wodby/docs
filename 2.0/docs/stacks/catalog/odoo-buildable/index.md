---
description: Deploy Odoo with your own and community modules on Wodby with the buildable Odoo stack, which builds Odoo with the modules and packages in your Git repository.
---

# Odoo (buildable)

The buildable Odoo stack runs [Odoo](https://www.odoo.com/) Community Edition 20, 19 or 18 built from your Git
repository: the repository holds your own and community modules and the Python packages they need. The stack has the
same services as the [Odoo stack](../odoo/index.md): Nginx, PostgreSQL, shared NFS storage for Odoo's files, and an
optional OpenSMTPD service. Its composition is documented in
[`wodby/stack-odoo-buildable`](https://github.com/wodby/stack-odoo-buildable).

Everything in the [Odoo guide](../odoo/index.md) applies, from the administrator settings to workers, mail and backups.
This page covers what differs.

## Repository

Start the repository from the [Odoo boilerplate](https://github.com/wodby/odoo-boilerplate) and connect it when you
create the app.

| Path | Purpose |
| --- | --- |
| `addons/` | Your modules, one directory per module with its `__manifest__.py` |
| `requirements.txt` | Python packages your modules need |

Modules can also live in other directories up to three levels deep, for example one directory per module collection
copied from a community repository. Every directory that holds modules is added to Odoo's addons path; the build log
shows the addons path and the modules it found.

## Build

Choose the Odoo version when you create the app. The build starts from Wodby's Odoo image for that version, copies the
repository into it and installs `requirements.txt`. Lines like `git+https://...` work. The image has no compiler, so
packages need prebuilt wheels.

The build fails when a module has the name of one of Odoo's own modules, because Odoo would ignore it.

## Modules

- The first deployment installs Odoo with the apps in the **Apps to install** setting, which can include your own
  modules.
- Later deployments update the installed modules whose files changed in the repository, or whose manifest version went
  up.
- New modules appear in Odoo's **Apps** menu; install them there.
- Uninstall a module in Odoo before you remove it from the repository.

Odoo Enterprise modules go in the repository like any other module; they need an Odoo Enterprise subscription.

## Updates

Odoo's exact build comes from the service's Odoo image, not from the repository. It moves forward with service updates,
and the app's next build uses it.

To run Odoo without your own modules, use the [Odoo stack](../odoo/index.md).
