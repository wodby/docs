---
description: Deploy Keycloak with your own themes and providers on Wodby with the buildable Keycloak stack, which builds Keycloak with the themes and provider jars in your Git repository.
---

# Keycloak (buildable)

The buildable Keycloak stack runs [Keycloak](https://www.keycloak.org/) built from your Git repository: the repository
holds your own login, account, email or admin themes and your custom providers. The stack has the same services as the
[Keycloak stack](../keycloak/index.md): Keycloak and PostgreSQL. Its composition is documented in
[`wodby/stack-keycloak-buildable`](https://github.com/wodby/stack-keycloak-buildable).

Everything in the [Keycloak guide](../keycloak/index.md) applies, from the administrator account to the hostname and
backups. This page covers what differs.

## Repository

Start the repository from the [Keycloak boilerplate](https://github.com/wodby/keycloak-boilerplate) and connect it
when you create the app.

| Path | Purpose |
| --- | --- |
| `themes/` | Your themes, one directory per theme with a directory per type, such as `login/theme.properties` |
| `providers/` | Your provider jars, such as authenticators, user storage, event listeners or protocol mappers |

A `login/theme.properties` that extends Keycloak's theme can start with:

```
parent=keycloak.v2
import=common/keycloak
styles=css/login.css css/my-theme.css
```

## Build

Choose the Keycloak version when you create the app. The build starts from the official Keycloak image of that
version, adds your themes and providers, and runs Keycloak's build with the service's settings, so Keycloak starts
without rebuilding.

The build fails when a theme has the name of one of Keycloak's own themes (`base`, `keycloak`, `keycloak.v2`) or has no
`theme.properties`. Build provider jars for the Keycloak version you run.

## Themes

Select a theme for a realm in Keycloak's administration console, under **Realm settings > Themes**. Themes are part of
the image, so changes reach Keycloak with the next deployment.

To run Keycloak without your own themes or providers, use the [Keycloak stack](../keycloak/index.md).
