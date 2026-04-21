# Certificates

Wodby manages TLS certificates for endpoint domains and shows certificate inventory at the organization level.

## What exists today

- Technical domains under `wodby.app` receive managed Let's Encrypt certificates automatically.
- When you add a custom domain from `Apps > [Instance] > Endpoints > Domains`, the available TLS modes are `Let's Encrypt` and `None`.
- Wodby automatically renews managed Let's Encrypt certificates before they expire.
- `Organization > Certificates` shows issued certificates, issuer, key type, status, issue date, renewal date, expiry date, and where each certificate is used.
- The organization certificate list can include certificates used by application domains and supported database resources.

## Current limitation

Custom certificate upload is coming soon.

## Planned direction

Once custom certificates ship, the intended model is:

- manage certificates at the organization level
- select an existing organization certificate from an endpoint or other supported resource

## Related pages

- [Organization](org.md)
- [Endpoints](apps/endpoints.md)
- [Service certificates](services/certs.md)
