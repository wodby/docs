# Domains

## Technical .wod.by domain name

Wodby provides a short *.wod.by domain name to every application, it depends on the name of the application and the name of the organization. It looks like this: 
```
[instance].[app name].[organization name].wod.by
```
you can find your technical domain from `Instance > Domains page`.

You can restrict access to technical domains by:

* Disabling domain
* Setting basic auth for this domain

## Attaching custom domain name

You can attach your custom domain name by following these steps:

1. Go to `Domains > Add` on your instance page
2. Add your domain
3. Add an A record targeted to your server IP from your DNS provider's control panel
4. You're all set. Please note that DNS records propagation may take up to 24 hours

You can attach wildcard domains, e.g. `*.example.com`

## WWW redirects

If you want your www subdomain to automatically redirect to non-www domain or vise-versa, you can do it from a domain edit page by selecting one of the redirect actions. Please note, you must add both www and non-www domains manually before configuring WWW redirect actions.

## Basic auth

You can enable basic auth from Instance > Domains > Basic auth. Only single basic auth can be set up per instance but you can choose which domains you want to apply it to.

## Indexation by Search Robots

All technical `*.wod.by` domains are not indexed by search engines (header X-Robots-Tag). Additionally, you can optionally prevent indexation for your custom domains on domain edit/add pages.

## HTTPs

### Let's Encrypt Certificates

You can enable HTTPS for your custom domains by requesting a free SSL certificate from [Let's Encrypt](https://letsencrypt.org/). Navigate to `Domains` tab of your instance page and click on `Get certificate` in the list of domains (currently not available for *.wod.by domains). Choose a provider "Let's encrypt" and submit the form. Before requesting the certificate make sure that your domain already attached to the server where the instance is currently deployed.

Additionally you can enable redirect for all HTTP requests to HTTPS from a domain edit page.

!!! tip "Let's Encrypt certificates renewal"
    We automatically renew all certificates acquired via Let's Encrypt.

!!! warning "Let's Encrypt limitations"
    Let's Encrypt have some [rate limits](https://community.letsencrypt.org/t/rate-limits-for-lets-encrypt/6769) and [may not be trusted by old browsers](https://community.letsencrypt.org/t/which-browsers-and-operating-systems-support-lets-encrypt/4394)

### Custom SSL Certificates

It's not currently possible to upload certificates from the dashboard. Please contact us if you need to set up a custom SSL certificate.

### HSTS

Since infrastructure version >= 5.5.3 you can configure [HSTS](../infrastructure/hsts.md) per domain via three provided options:

* Disable
* Enable for this domain (default)
* Enable for this domain and all subdomains

Max age is `31536000` and cannot be changed.