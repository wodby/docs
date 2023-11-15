# Routes and domains

Routes are the way to publish access to your services inside and outside the kubernetes cluster. You can add/remove ports, publish ports or add custom domains via routes. 

## Technical domains

By default, Wodby will generate technical domains for services in your application that have enabled HTTP routes. The technical domains built in the following way – `<service-name>.<instance-name>.<app-name>.<org-name>.wodby.app`. We will also automatically issue Let's Encrypt certificates for technical domains. Additionally, the main service with http routes will have a technical domain without a service name – `<instance-name>.<app-name>.<org-name>.wodby.app`.

## SSL Certificates

Wodby provides a simple way to issue an SSL certificate for a domain in your HTTP route. Currently, we support only [Let's Encrypt](https://letsencrypt.org/) issuer. We will automatically renew Let's Encrypt certificates before they expire. You can also review all certificates that we issued from your organization settings page. 

### Custom certificates

We will support adding custom certificates but this functionality not yet implemented.
