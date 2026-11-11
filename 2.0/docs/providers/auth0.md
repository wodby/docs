---
description: Use the Auth0 provider in Wodby to inject your Auth0 domain and client credentials into app services and stacks as environment variables.
---

# Auth0

Auth0 is available in Wodby as a `variable` provider. Use it when you want to inject Auth0 domain and client credentials into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Domain | Yes | `AUTH0_DOMAIN` |
| Client ID | Yes | `AUTH0_CLIENT_ID` |
| Client Secret | Yes | `AUTH0_CLIENT_SECRET` |

To change the domain of an existing integration, enter the client secret again. Your application sends the secret to
that domain, so a new domain can't reuse it without you entering it.

## Usage

After you create an Auth0 integration and attach it to an app service or stack, Wodby injects the variables above into the container.
