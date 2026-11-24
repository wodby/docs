---
description: Deploy Redmine 7.0 or 6.1 on Wodby with the Redmine catalog stack, which runs it with PostgreSQL and shared NFS storage for attachments.
---

# Redmine stack guide

The Wodby Redmine catalog stack runs [Redmine](https://www.redmine.org/) 7.0 or 6.1 with PostgreSQL, shared NFS
storage for attachments, and an optional OpenSMTPD service for mail. The current composition is documented in
[`wodby/stack-redmine`](https://github.com/wodby/stack-redmine).

The stack needs no repository: Redmine comes with the service's image, ready to run.

## Administrator account

Redmine is installed during the app's first deployment. Set up the installation in the Redmine service's settings when
you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Admin password | none, required | The administrator's password, at least 8 characters |
| Admin login | `admin` | The administrator's login |
| Admin email | empty | The administrator's email address |
| Language | `en` | The language of the default trackers, statuses and roles, and of the administrator, such as `de` or `pt-BR` |

- Redmine's default `admin` account with the password `admin` never works: the first deployment gives it your login
  and password.
- Redmine's host name is set to the app's address, and its email sender to `noreply@` that address. Change both in
  **Administration › Settings**.

These settings are only used when Redmine is installed. To change the administrator later, use Redmine.

If the first deployment can't install Redmine, for example because the admin password is missing or too short, the
deployment's post-deploy step fails with the reason and nobody can sign in. Fix the setting and deploy again.

## Updates

Redmine updates arrive with new revisions of the service's image. Each deployment applies the database changes the new
version brings. To move to a newer Redmine version, change the Redmine service's version and deploy. Back up the app
first.

## Plugins and themes

The catalog stack runs Redmine without plugins or extra themes. To add them, build your own image from the service's
`wodby/redmine` image with the plugins in `/usr/src/redmine/plugins` and the themes in `/usr/src/redmine/themes`, and
use it from a custom service based on the [Redmine service](https://github.com/wodby/service-redmine). Each deployment
runs the plugins' database migrations.

## Workers

Each Redmine replica runs 2 worker processes with 5 threads each by default. Change the **Workers** setting to match the
service's memory; each worker uses about 150 MB.

## Mail

Enable the OpenSMTPD service to send Redmine's notifications through it, and attach an
[SMTP provider integration](../../../providers/smtp.md) for production delivery; see the
[OpenSMTPD guide](../opensmtpd/index.md). Without it, Redmine sends no email.

A restart or deployment never loses a notification. If the mail server can't be reached, the change is still saved and
the notification is not sent.

## Data and backups

- The `files` volume holds attachments. Every Redmine replica shares it through the NFS storage service.
- The PostgreSQL database holds everything else.

Back up both the database and the `files` volume; see [Application Backups](../../../apps/backups.md).

## Limits

- PostgreSQL only.
- Plugins and themes need your own image; see [Plugins and themes](#plugins-and-themes).
- Redmine's repository browser isn't supported: the stack has no storage for Git or Subversion repositories.
- The largest attachment is set by Redmine's **Maximum attachment size** setting in **Administration › Settings ›
  Files**.
