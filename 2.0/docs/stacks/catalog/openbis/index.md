---
description: Deploy openBIS, the lab notebook and inventory manager for research data, on Wodby with PostgreSQL, an Nginx entry point and optional email.
---

# openBIS stack guide

The Wodby openBIS catalog stack runs [openBIS](https://openbis.ch/), the lab notebook, inventory manager, and research
data management system. The stack needs no repository: openBIS comes ready to run. The current composition is
documented in [`wodby/stack-openbis`](https://github.com/wodby/stack-openbis).

| Service | What it does |
| --- | --- |
| openBIS | Runs openBIS's application server with the lab notebook, its data store server, and its file server. Stores files and data sets on its volume. Runs as one replica |
| Nginx | The app's entry point. Sends the app's domains to openBIS and `/` to the lab notebook |
| PostgreSQL | Stores openBIS's three databases |
| OpenSMTPD | Sends openBIS's email. Disabled by default |

## Admin account

openBIS's administrator is the user `admin`. Set its password in the openBIS service's **Admin password** setting when
you create the app; it needs at least 12 characters.

The first deployment creates openBIS's databases and the lab notebook's default spaces and settings, which takes a few
minutes. Open the app's main route, which redirects to the lab notebook, and sign in as `admin`.

openBIS sets the admin password from the setting on every start. To change it, change the setting and deploy the
openBIS service. Add other users in openBIS.

## Databases

openBIS keeps its data in three PostgreSQL databases on the stack's PostgreSQL service: the environment's database and
two more named after it with `_messages` and `_pathinfo` at the end. Wodby creates the two extra databases when it
deploys openBIS and gives openBIS's database user access to them.

openBIS commits changes that span its servers with PostgreSQL's two-phase commit. The stack turns this on for its
PostgreSQL service (**Max prepared transactions** 64). Keep it above 0: without it, those changes fail.

openBIS supports only the stack's PostgreSQL service, not a managed PostgreSQL server.

## Mail

openBIS sends password resets and notifications by email. The OpenSMTPD service is disabled by default. When you
enable it, openBIS sends through OpenSMTPD from `noreply@` and the app's primary domain. Attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production delivery, and make sure your
provider accepts that sender. See the [OpenSMTPD guide](../opensmtpd/index.md).

## Uploads

Uploads have no size limit, and requests may take up to an hour. openBIS's own clients split large files into parts.

## Data and backups

The openBIS service's volume (20 GB by default) holds the files and data sets you store in openBIS, and openBIS's
configuration. The PostgreSQL service's volume holds the databases.

Back up the PostgreSQL service with its database backup. It covers the environment's main database only, not the
`_messages` and `_pathinfo` databases. When you restore it, those two databases start empty: restart the openBIS
service afterwards so it sets them up again. The openBIS service's volume has no Wodby backup. See
[Backups](../../../apps/backups.md).

## Memory

openBIS needs about 3 GB of memory and may use up to 7 GB. Use nodes with at least 8 GB of memory.

## Upgrades

A newer openBIS version migrates its databases when it starts. Back up the databases and keep a copy of the openBIS
service's volume first. Moving back to an older version is not supported.

## Limits

- openBIS runs as one replica.
- Wodby backups cover only the main database, and a new environment, such as a preview, starts with empty `_messages`
  and `_pathinfo` databases.
- Managed PostgreSQL servers are not supported.
- openBIS's SFTP and RO-Crate servers are not included.
