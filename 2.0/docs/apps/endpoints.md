# Endpoints

Endpoints represent accessible endpoints to your app services. Endpoints consist of domains and/or ports. You can add configure domains, add custom domains, issue TLS certificates for a domain, publish/unpublish ports. 

## Domains

### Technical domains

By default, Wodby will generate technical domains for services in your application that have enabled HTTP routes. The technical domains built in the following way – `<service-name>.<instance-name>.<app-name>.<org-name>.wodby.app`. We will also automatically issue Let's Encrypt certificates for technical domains. Additionally, the main service with http routes will have a technical domain without a service name – `<instance-name>.<app-name>.<org-name>.wodby.app`.

### SSL Certificates

Wodby provides a simple way to issue a SSL (TLS) certificate for a domain in your endpoint. Currently, we support only [Let's Encrypt](https://letsencrypt.org/) issuer. We will automatically renew Let's Encrypt certificates before they expire. You can also review all certificates that we issued from your organization settings page. 

Custom certificates not currently supported.

### Settings

You can add so-called _Setting_ to your domains which represent individual configuration via [Ingress Nginx annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/).

### Auths

You can set up basic auth for your app (or for the specific app service or for the specific domain) from _"Apps > [App instance] > Endpoints > Auths"_` page. 

## Ports

Endpoint ports allow you to publish/unpublish a port that a service define. Ports have a protocol (`UDP` or `TCP`) and a port number.

