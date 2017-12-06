# SSL

## Free Let's Encrypt Certificates
 
You can enable HTTPS for your custom domains by requesting a free SSL certificate from [Let's Encrypt](https://letsencrypt.org). Navigate to `Cloud hosting Domains` and click on `Get certificate` in the list of domains (not available for `*.wod.by` domains). Choose a provider `Let's encrypt` and submit the form. Before requesting the certificate make sure that your domain already attached to the server where the instance is currently deployed.  

Additionally you can enable redirect for all HTTP requests to HTTPS from a domain edit page.
 
Notes: 

* We automatically renew all certificates acquired via Let's Encrypt. 
* Let's Encrypt have some [rate limits](href="https://community.letsencrypt.org/t/rate-limits-for-lets-encrypt/6769)
* Let's Encrypt certificates [may not be trusted by old browsers](https://community.letsencrypt.org/t/which-browsers-and-operating-systems-support-lets-encrypt/4394)

## Custom SSL Certificates

It's not currently possible to upload certificates from the dashboard. Please [contact us](../product/support.md) if you need to set up a custom SSL certificate.

## HSTS

Since [infrastructure version](/infrastructure/versioning.md) >= 5.5.3 you can configure [HSTS](/infrastructure/hsts.md) per domain via three provided options:

* Disable
* Enable for this domain (default)
* Enable for this domain and all subdomains

Max age is `31536000` and can't be changed.