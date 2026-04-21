# Endpoints

Endpoints are the public or private entry points to your app services. They consist of domains and/or published ports.

From `Apps > [Instance] > Endpoints` you can manage four areas:

- `Domains`
- `Ports`
- `Settings`
- `Auths`

## Domains

The `Domains` screen is used for HTTP endpoints.

### Technical domains

By default, Wodby generates technical domains for app services that expose HTTP routes.

The default pattern is:

- `<service-name>.<instance-name>.<app-name>.<org-name>.wodby.app`

The main service with HTTP routes also gets a shorter technical domain:

- `<instance-name>.<app-name>.<org-name>.wodby.app`

Wodby automatically issues and renews Let's Encrypt certificates for these technical domains.

### Custom domains

From the dashboard you can add a custom domain to an HTTP app service endpoint.

When creating a domain, you choose:

- app service
- endpoint
- port
- domain name
- TLS mode: `Let's Encrypt` or `None`
- whether the domain should be `Main`
- whether the domain should be `Primary`

Only services with HTTP endpoints are available in this flow.

### Main and primary

Wodby distinguishes between two default-domain flags:

- `Main` is the main domain for the whole app instance
- `Primary` is the default domain for a specific app service endpoint

Main domains are always primary. In practice:

- an app instance has one main domain
- each app service can have its own primary domain

### TLS certificates

Wodby can issue TLS certificates for endpoint domains. For public docs, treat [Let's Encrypt](https://letsencrypt.org/) as the supported issuer for managed certificate flows today. Wodby automatically renews Let's Encrypt certificates before they expire.

You can review certificates issued for your organization's applications from [Certificates](../certs.md).

Custom certificate upload is coming soon. The planned model is organization-level certificate management with endpoint-level selection.

### Domain status and private domains

The domain list shows status, certificate issuer, and whether a domain is main or primary.

You may also see private domains generated for internal use. Those are not managed the same way as regular public custom domains.

### Settings

The `Settings` screen manages ingress behavior for HTTP endpoints.

Settings map to [Ingress Nginx annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/) and let you control routing behavior without editing Kubernetes manifests manually.

Each setting has:

- annotation name, without the `nginx.ingress.kubernetes.io/` prefix
- value
- optional app service scope
- optional domain scope

This gives you three practical scopes:

- app-level, when both service and domain are left empty
- service-level, when a service is selected and domain is left empty
- domain-level, when a specific domain is selected

Wodby applies ingress settings from least specific to most specific, so domain-specific settings override service-level settings, and service-level settings override app-level settings.

### Auths

The `Auths` screen manages HTTP basic authentication.

Each auth entry has:

- username
- password
- optional realm
- optional app service scope
- optional domain scope

This gives you the same three practical scopes:

- app-level, when both service and domain are left empty
- service-level, when a service is selected and domain is left empty
- domain-level, when a specific domain is selected

Auth precedence is most-specific first:

- domain auth overrides service auth
- service auth overrides app-level auth

The edit screen can also reveal the current password for an existing auth entry.

## Ports

The `Ports` screen lists endpoint ports defined by your app services.

Each port has:

- app service
- endpoint name
- protocol
- internal port number
- optional public port

### Publishing ports

Manual port publishing is intended for non-HTTP ports such as SSH or other TCP or UDP services.

- HTTP exposure is handled through domains, not through manual public-port publishing
- only non-private, non-HTTP ports can be published or unpublished from this screen
- after publishing, Wodby may need to redeploy the cluster ingress-nginx app before the public port becomes available

When a port is published, the dashboard shows the assigned public port. For SSHD services, it also shows ready-to-use `ssh`, `sftp`, and `scp` command examples based on the app instance main domain.

If you plan to use published SSH ports, see [SSH keys](../user/ssh-keys.md).
