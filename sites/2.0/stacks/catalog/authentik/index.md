Source: https://wodby.com/docs/2.0/stacks/catalog/authentik/

# authentik stack guide

The Wodby authentik catalog stack runs [authentik](https://goauthentik.io/), the open source identity provider for
single sign-on with OAuth2, OpenID Connect, SAML, LDAP and more. It runs the official authentik image as a server and a
worker, with PostgreSQL, shared file storage, and an optional OpenSMTPD service for mail. The current composition is
documented in [`wodby/stack-authentik`](https://github.com/wodby/stack-authentik).

| Service | What it does |
| --- | --- |
| authentik | Serves the user and admin interfaces, the API, and the sign-in flows |
| Worker | Runs authentik's background tasks, such as blueprints, email, and directory synchronization. Required |
| PostgreSQL | Stores users, applications, providers, flows, sessions, authentik's cache, and its task queue |
| Shared file storage | Holds uploaded icons, logos, backgrounds, and reports for the server and the worker |
| OpenSMTPD | Sends authentik's email. Disabled by default |

## Administrator account

Set the first administrator in the authentik service's settings when you create the app. Both settings are required:

| Setting | What it sets |
| --- | --- |
| Admin email | The email address of the `akadmin` administrator |
| Admin password | The administrator's password |

The first deployment creates the `akadmin` user in the `authentik Admins` group. Because this account has a password,
authentik's initial setup page is closed, so nobody else can claim a new installation.

Open the app's main route and sign in with `akadmin` or the admin email, and the admin password. The admin interface is
at `/if/admin/`.

The settings are only used when the administrator is created. Changing them later does not change the account. Change
the password, and add other people, in authentik.

## Connect your applications

In the admin interface, create a provider, for example **OAuth2/OpenID Provider** or **SAML Provider**, and an
application that uses it, under **Applications > Applications**. For OpenID Connect, the issuer of an application with
the slug `my-app` is `https://<your-domain>/application/o/my-app/`, and the discovery document is at
`/application/o/my-app/.well-known/openid-configuration`.

To protect an app that has no sign-in of its own, use a **Proxy Provider** with authentik's embedded outpost, which runs
in the authentik service.

## Domain and base URL

authentik uses the environment's primary URL as its base URL, which it uses for links in emails and other places
outside a request. authentik stores it the first time it starts. After you add a domain or change the primary domain,
update the base URL under **System > Settings** in authentik. See [Domains](https://wodby.com/docs/2.0/apps/endpoints/#domains).

TLS ends at Wodby's router, and authentik builds `https://` addresses from the request's domain.

## Mail

authentik sends password recovery, email verification, and notification emails. The OpenSMTPD service is disabled by
default. Either enable it, or set your own SMTP server with `AUTHENTIK_EMAIL__*` environment variables on the authentik
service. See [Environment variables](https://wodby.com/docs/2.0/apps/environment-variables/).

While authentik is linked to OpenSMTPD, it sends from `noreply@` and the primary domain. Attach an
[SMTP provider integration](https://wodby.com/docs/2.0/providers/smtp/) to OpenSMTPD for production delivery, and make sure your
provider accepts that sender. See the [OpenSMTPD guide](https://wodby.com/docs/2.0/stacks/catalog/opensmtpd/).

## Change configuration

Add or change `AUTHENTIK_*` environment variables on the authentik service and deploy it. The worker gets the same
variables. Manage applications, providers, flows, policies, and users in the admin interface or the API.

The `secret_key` token in **Configuration > Tokens** signs cookies and sessions. Changing it signs everyone out. See
[Tokens](https://wodby.com/docs/2.0/apps/tokens/).

## Resources and replicas

The authentik server requests 0.2 CPU and 768 MB of memory, with a 1.5 GB memory limit. The worker requests 0.1 CPU and
384 MB of memory, with a 1 GB memory limit. Change them in **Runtime > Resources**. See
[Resources tab](https://wodby.com/docs/2.0/apps/services/#resources-tab).

You can run several replicas of the server and the worker. They share the database and the file storage. See
[Replicas](https://wodby.com/docs/2.0/apps/services/#replicas).

## Data and backups

PostgreSQL (10 GB by default) holds authentik's data. The shared file storage (5 GB volume) holds uploaded files.
Back up the PostgreSQL database and the shared file storage to keep a complete installation. See
[Backups](https://wodby.com/docs/2.0/apps/backups/) and [Imports](https://wodby.com/docs/2.0/apps/imports/).

## Upgrades

authentik migrates its database when a newer version starts and refuses to skip a version. Back up the PostgreSQL
database, then choose the next version on the
[General configuration](https://wodby.com/docs/2.0/apps/services/#general-configuration) tab or upgrade the stack. Moving back to an
older version is not supported: restore the backup instead.

## Limits

- authentik can't deploy outposts to the cluster. The embedded outpost serves proxy providers. Run other outposts, such
  as LDAP or RADIUS, yourself and connect them to authentik.
- Wodby delivers new authentik releases as new versions of the service, so authentik's own update check is off.
