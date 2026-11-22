---
description: Deploy Plane project management on Wodby with the Plane catalog stack, which runs it with PostgreSQL, Valkey, RabbitMQ and Silo storage.
---

# Plane stack guide

The Wodby Plane catalog stack runs [Plane](https://plane.so/) Community Edition project management with PostgreSQL,
Valkey, RabbitMQ, Silo for uploaded files, and an optional OpenSMTPD service for mail. The current composition is
documented in [`wodby/stack-plane`](https://github.com/wodby/stack-plane).

The stack needs no repository: Plane runs from its own images.

## Before you create the app

- Plane, PostgreSQL, Valkey, RabbitMQ and Silo are required. OpenSMTPD is optional and not selected by default.
- The Plane service runs several processes: the web app, the admin app, published projects, real-time editing, the
  API, background workers and a scheduler. Together they request about 1.2 GiB of memory, before PostgreSQL and the
  other services.
- A new app takes several minutes before Plane answers, while it prepares its database.

## Administrator account

Set the instance administrator in the Plane service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| **Admin email** | none, required | The email address the administrator signs in with |
| **Admin password** | none, required | The administrator's password. Plane accepts only strong passwords, such as four unrelated words and a number |
| **Admin first name** | `Admin` | The administrator's first name |
| **Allow sign-up** | `0` | `1` lets anyone who can reach Plane create an account |

The first deployment creates the administrator before Plane serves any page, so Plane's instance setup page is never
offered to visitors. If the password is missing or too weak, the deployment fails with the reason and nothing is
installed; fix the setting and deploy again.

1. Open the app's main domain and sign in with **Admin email** and **Admin password**, then create your first
   workspace.
2. Open `/god-mode` on the same domain to manage instance settings, such as sign-up, sign-in methods and email.

These settings are only used when Plane is installed. Change the administrator and instance settings in Plane
afterwards.

## Updates

Plane updates arrive with new revisions of the Plane service. Each deployment applies the database changes the new
release brings before the API starts. Back up the app before you deploy a new release.

## Uploads

Images and attachments are stored in Silo, an S3-compatible storage service in the same app, and reach browsers through
Plane's own address. Uploads are limited to 5 MB.

## Mail

Enable the OpenSMTPD service to send invitations and notifications through it, and attach an
[SMTP provider integration](../../../providers/smtp.md) for production delivery; see the
[OpenSMTPD guide](../opensmtpd/index.md). You can also set up an outgoing mail server in God Mode.

## Data and backups

- The PostgreSQL database holds projects, work items, pages and users.
- Silo's `data` volume holds uploaded images and attachments.
- RabbitMQ and Valkey hold only queued jobs and cache.

Back up both the database and Silo's `data` volume; see [Application Backups](../../../apps/backups.md).

## Limits

- Plane Community Edition only.
- Uploads are stored in the app's Silo service; external S3 storage isn't supported.
- Plane's own images are used as they are, so custom code and plugins aren't supported.
