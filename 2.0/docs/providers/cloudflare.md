# Cloudflare

Cloudflare is available in Wodby as a `variable` provider. Use it when you want to inject Cloudflare site and secret keys into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Site Key | Yes | `CLOUDFLARE_SITE_KEY` |
| Secret Key | Yes | `CLOUDFLARE_SECRET_KEY` |

## Usage

After you create a Cloudflare integration and attach it to an app service or stack, Wodby injects the variables above into the container.
