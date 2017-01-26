# Domains

* [Default .wod.by domain name](#default-wodby-domain-name)
* [Attaching custom domain name](#attaching-custom-domain-name)
* [HTTPS (SSL via Let's Encrypt)](#https-ssl-via-lets-encrypt)
* [WWW redirects](#www-redirects)
* [Basic auth](#basic-auth)
* [Indexation by Search Robots](#indexation-by-search-robots)

## Default .wod.by domain name

Wodby provides a short `*.wod.by` domain name to every application, it depends on the name of the application and the name of the organization. It looks like this: `[instance].[app name].[organization name].wod.by`

For exact domain name look at the "Domain" tab of the instance page.  

## Attaching custom domain name

You can attach your custom domain name by following these steps:

1. Go to `Domains > Add` on your instance page

2. Add your domain

3. Add `A record` with Wodby's IP address in your DNS provider's control panel

4. You're all set. However, DNS records propagation takes up to 24 hours
 
## HTTPS (SSL via Let's Encrypt)
 
You can enable HTTPS for your custom domains by requesting a free certificate from <a href="https://letsencrypt.org" target="_blank">Let's Encrypt</a>. Navigate to `App page > Domains` and click on `Get certificate` in the list of domains (not available for `*.wod.by` domains). Choose a provider `Let's encrypt` and submit the form. 
 
> We automatically renew all certificates acquired via Let's Encrypt.
 
Before requesting the certificate please double `check that your domain already attached to the server` where it was deployed via Wodby.  
 
> Let's Encrypt have some rate limits. Read <a href="https://community.letsencrypt.org/t/rate-limits-for-lets-encrypt/6769" target="_blank">this article</a> to learn more.

Additionally you can enable redirect for all HTTP requests to HTTPS on domain edit page.

> Let's Encrypt certificates may not be trusted by old browsers, please see <a href="https://community.letsencrypt.org/t/which-browsers-and-operating-systems-support-lets-encrypt/4394" target="_blank">this article</a> for details.

## WWW redirects

If you want your www subdomain to automatically redirect to non-www domain or vise-versa, you can do it from a domain edit page by selecting one of the redirect actions. Please note, you must add both www and non-www domains manually before configuring WWW redirect actions.

## Basic auth

You can enable basic auth for all domains of an app instance from `[Instance] > Domains > Basic auth`

## Indexation by Search Robots

All technical `*.wod.by` domains are not indexed by search engines (header X-Robots-Tag). Additionally, you can optionally prevent indexation for your custom domains on domain edit/add pages.