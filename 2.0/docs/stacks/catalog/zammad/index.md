---
description: Deploy the Zammad helpdesk on Wodby with the Zammad catalog stack, which runs it with PostgreSQL, Redis, Memcached, Elasticsearch and OpenSMTPD.
---

# Zammad

The Wodby Zammad catalog stack runs the [Zammad](https://zammad.org/) helpdesk with PostgreSQL, Redis, Memcached,
Elasticsearch, and an OpenSMTPD mail relay. The current services and defaults are documented in
[`wodby/stack-zammad`](https://github.com/wodby/stack-zammad).

## Before you create the app

- Zammad, PostgreSQL, Redis, and Memcached are required. Elasticsearch and OpenSMTPD are optional and selected by
  default.
- The Zammad service runs four processes: the web server, the web application, the WebSocket server, and the background
  worker. Together they request about 1 CPU and 2 GiB of memory, before PostgreSQL, Elasticsearch, and the other
  services.
- Set **Administrator email** on the Zammad app service. It is required. See the next section.

A new app takes a few minutes before its domain answers, while Zammad installs its database.

## Administrator account

Set the first administrator in the Zammad service's settings when you create the app:

| Setting | What it sets |
| --- | --- |
| **Administrator email** | The email address the administrator signs in with. Required. |
| **Administrator first name** | The administrator's first name. `Admin` by default. |
| **Administrator last name** | The administrator's last name. |

Wodby generates the password as the `admin_password` token. During the first deployment, before Zammad serves any page,
Wodby creates the administrator with the Admin and Agent roles and access to all groups. Zammad's getting started page,
which lets the first visitor create the administrator, is never offered.

1. Open the Zammad app service's **Configuration > Tokens** tab and reveal `admin_password`. See
   [Tokens](../../../apps/tokens.md).
2. Open the app's main domain and sign in with **Administrator email** and that password.
3. Change the password under **Profile**, then set your organization name and connect your mailboxes.

The settings and the token are used only while no administrator exists. Changing them later does not change an existing
administrator; change it in Zammad under **Profile** or **Admin > Users**.

If the email already belongs to another Zammad user, the administrator is not created and the deployment does not
finish. Set another email and deploy again.

Customers can register themselves by default (**Register as a new customer**). Turn this off under
**Admin > Security > Base** if customers must not sign up.

## Search with Elasticsearch

Zammad uses Elasticsearch for search. It needs a supported Elasticsearch version, and the catalog Elasticsearch
service provides one. OpenSearch is not supported by Zammad. See
[Zammad's Elasticsearch requirements](https://docs.zammad.org/en/latest/install/elasticsearch.html).

The Elasticsearch service is optional. Without it, Zammad searches the database, which is slower and less complete. To
save resources, leave it out when you create the app. To turn Elasticsearch off while the service is still linked, set
the environment variable `ELASTICSEARCH_ENABLED` to `false` on the Zammad app service.

Wodby writes Zammad's Elasticsearch settings on every deployment, from the link, so changes made to them in Zammad are
overwritten. When no search index exists, the deployment builds one.

## Mail

Zammad sends agent notifications through its notification channel. While the Zammad app service is linked to OpenSMTPD,
Wodby points Zammad's unconfigured notification channel at the relay. For production delivery, attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD. See the [OpenSMTPD guide](../opensmtpd/index.md).

You can also set your mail provider's SMTP server as the notification sender directly in Zammad under
**Admin > Channels > Email**. Wodby never changes a notification channel that you have configured in Zammad.

Incoming email is not configured by Wodby. To turn messages into tickets, add your mailboxes under
**Admin > Channels > Email**. See
[Zammad's email channel documentation](https://admin-docs.zammad.org/en/latest/channels/email/index.html).

## Domains

Zammad builds links in notifications from the app service's primary domain, and only allows live connections from it.
Wodby sets this address on every deployment, so changes made to it in Zammad are overwritten. After you change the
primary domain, deploy the Zammad app service again.

The browser keeps WebSocket connections open, so the route has no request timeout by default. Do not set the route's
request body size: it makes the route hold each request in memory until it is complete, and live connections stop
working. See [HTTP settings](../../../apps/endpoints.md#http-settings).

## Change configuration

Add environment variables through the Zammad app service's **Additional Zammad environment variables** integration,
then deploy. Every Zammad process receives them. Useful ones include `TZ`, `ZAMMAD_WEB_CONCURRENCY`, `MAX_THREADS`, and
`ZAMMAD_PROCESS_DELAYED_JOBS_WORKERS`. See [Environment variables](../../../apps/environment-variables.md).

## Data and backups

- PostgreSQL (20 GB volume by default) holds tickets, users, settings, and attachments.
- Elasticsearch (10 GB volume by default) holds the search index, which Zammad can rebuild from the database.
- Redis has a 1 GB volume. Memcached keeps its cache in memory only.
- The Zammad service has no volume.

Zammad stores attachments in the database by default, so back up the PostgreSQL database. The PostgreSQL service has
backup and import operations in Wodby. The Zammad, Redis, Memcached, Elasticsearch, and OpenSMTPD services have none.
See [Backups](../../../apps/backups.md) and [Imports](../../../apps/imports.md).

To keep attachments in S3-compatible storage instead, add the `S3_URL` variable through the
**Additional Zammad environment variables** integration, deploy, then choose S3 under **Admin > System > Storage**. See
[Zammad's storage settings](https://admin-docs.zammad.org/en/latest/settings/system/storage.html). File system storage
is not supported, because Zammad's processes share no volume. With S3, back up the bucket together with the database.

## Limits

- Every Zammad process runs one replica, and the service does not scale. The background worker must never run twice, so
  it is replaced, not updated in place, on each deployment.
- Imports from other helpdesks (OTRS, Zendesk, Freshdesk, Kayako) on Zammad's getting started page are not available,
  because Wodby has already set up the system.
