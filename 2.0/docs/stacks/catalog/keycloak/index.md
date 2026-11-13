---
description: Deploy Keycloak in production mode with a PostgreSQL database on Wodby with the Keycloak catalog stack, and sign in with the generated admin password.
---

# Keycloak

The Wodby Keycloak catalog stack runs Keycloak in production mode with a PostgreSQL database. The current composition is
documented in [`wodby/stack-keycloak`](https://github.com/wodby/stack-keycloak).

## Your own themes and providers

To add your own login, account or email themes, or custom providers, use the
[buildable Keycloak stack](../keycloak-buildable/index.md) instead. You keep them in a Git repository
started from the [Keycloak boilerplate](https://github.com/wodby/keycloak-boilerplate), and Wodby builds Keycloak with
them on every push. Select a theme for a realm under **Realm settings > Themes**.

## First sign-in

Open the app's main route. Sign in with the `admin_username` token, which is `admin`, and the generated `admin_password`
token. Find both on the Keycloak app service's **Configuration > Tokens** tab. See [Tokens](../../../apps/tokens.md).

Keycloak creates this account only on the first start with an empty database, and marks it as temporary. Changing the
tokens later does not change an existing account.

## Hostname and TLS

Keycloak uses the environment's primary URL for the addresses it issues, such as token issuers and redirects. TLS ends
at Wodby's router.

## Change configuration

Add or change `KC_*` environment variables on the app service and deploy it. Environment variables take precedence over
`conf/keycloak.conf`, which is not stored on a volume. Database connection values come from the PostgreSQL link. See
[Environment variables](../../../apps/environment-variables.md).

Manage realms, clients, and users in the Keycloak administration console or its API.

## Data and backups

Keycloak has no volume. All of its data is in the linked PostgreSQL database (20 GB volume by default), so back up that
database. See [Backups](../../../apps/backups.md).

## Limits

- Keycloak serves health and metrics on a private management port (9000). It has no public route.
- The Keycloak service is not scalable.
