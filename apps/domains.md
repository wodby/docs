# Domains

## Technical .wod.by domain name

Wodby provides a short `*.wod.by` domain name to every application, it depends on the name of the application and the name of the organization. It looks like this: `[instance].[app name].[organization name].wod.by`, you can find your technical domain from `Application > Domains` page.

## Attaching custom domain name

You can attach your custom domain name by following these steps:

1. Go to `Application > Domains > Add` on your instance page
2. Add your domain
3. Add an `A record` with Wodby's IP address from your DNS provider's control panel
4. You're all set. Please note that DNS records propagation may take up to 24 hours

## WWW redirects

If you want your www subdomain to automatically redirect to non-www domain or vise-versa, you can do it from a domain edit page by selecting one of the redirect actions. Please note, you must add both www and non-www domains manually before configuring WWW redirect actions.

## Basic auth

You can enable basic auth for all domains of an app instance from `Application > Domains > Basic auth`

## Indexation by Search Robots

All technical `*.wod.by` domains are not indexed by search engines (header X-Robots-Tag). Additionally, you can optionally prevent indexation for your custom domains on domain edit/add pages.

## HTTPs

Please see [this article](ssl.md).
