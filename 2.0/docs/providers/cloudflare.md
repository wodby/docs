# Cloudflare

Cloudflare supports two integration types in Wodby:

- `application_access` publishes and protects app HTTP endpoints with Cloudflare Tunnel and Cloudflare Access
- `variable` injects Cloudflare Turnstile keys into app services or stacks

Create separate integrations when you need both types. Each integration has one selected type and only asks for the
fields required by that use case.

## Application Access

### Before creating the integration

1. Copy the `Account ID` from the Cloudflare dashboard. See
   [Find account and zone IDs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/).
2. Open `My Profile > API Tokens` and create a custom **User API Token**. Do not use
   `Manage Account > Account API Tokens`; its account-scoped policy editor does not expose the required zone
   permission rows.
3. Under `Permissions`, use `Add more` for each Account permission row:
   - `Cloudflare One Connector: cloudflared`: Edit
   - `Access: Apps`: Edit
   - `Access: Policies`: Edit
4. Use `Add more` again for each Zone permission row:
   - `Zone`: Read
   - `DNS`: Edit
5. Under `Account Resources`, include the intended Cloudflare account. Under `Zone Resources`, include only the zones
   Wodby may publish.
6. Open `Zero Trust > Access controls > Policies` and create at least one reusable `Allow` policy. Wodby lists reusable
   policies; the per-application policy editor is not used for this selection.

The integration form asks for the Account ID and API token. Wodby checks authentication and the base publishing
permissions when you create the integration, and reports whether the token is invalid or a particular permission is
missing. Wodby does not request certificate permissions.

### Configure an app

Select Protected mode during app creation, or open `Apps > [App] > [Instance] > Settings > Access`. Choose:

- the Cloudflare Application Access integration
- Entire app or Selected endpoints scope
- a DNS zone that the token can manage
- Flattened or Hierarchical hostname structure; the form previews the resulting additional-service hostnames
- an existing reusable Access policy
- the primary hostname in the selected zone

#### Hostname structures

| Structure | Primary example | Additional endpoint example | Certificate requirement |
| --- | --- | --- | --- |
| Flattened | `dev-cms.example.com` | `mailpit-dev-cms.example.com` | Cloudflare Universal SSL; this is the default |
| Hierarchical | `dev.cms.example.com` | `mailpit.dev.cms.example.com` | Active Advanced certificate for `dev.cms.example.com` and `*.dev.cms.example.com` |

Hierarchical hostnames require
[Cloudflare Advanced Certificate Manager](https://developers.cloudflare.com/ssl/edge-certificates/advanced-certificate-manager/).
When Hierarchical is selected, Wodby shows a warning but does not order or inspect certificates. Before using the
generated hostnames, create a customer-managed Advanced certificate covering the exact primary hostname and its
wildcard children, then wait for it to become active.
[Total TLS](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/total-tls/) does not issue
certificates for Cloudflare Tunnel hostnames. See
[Primary hostname](../apps/access.md#primary-hostname).

Wodby creates one protected hostname per distinct enabled external HTTP destination and manages the cloudflared tunnel,
tunnel connector credentials, DNS records, and Cloudflare Access application. It
attaches the selected reusable policy, but the policy itself remains customer-managed and determines who may sign in.

When access is removed or the app instance is deleted, Wodby removes the connector, tunnel connections, managed DNS
records, tunnel, and Access application. It does not delete the selected reusable Access policy, DNS zone, or any
customer-managed certificate. If a managed DNS record no longer has Wodby's ownership marker and expected tunnel
target, Wodby leaves it untouched and reports a cleanup warning. Temporary API failures are retained as retryable
cleanup obligations on the integration page; keep the integration and its permissions available until cleanup
finishes.

Wodby does not use Cloudflare Quick Tunnels or `*.trycloudflare.com` hostnames for App Access. Quick Tunnels generate
random temporary addresses, are intended for testing and development, and have no uptime guarantee. Stable production
publication uses a managed tunnel and hostnames in the selected Cloudflare zone. See
[Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/).

### Troubleshooting TLS

`ERR_SSL_VERSION_OR_CIPHER_MISMATCH` normally means the selected Cloudflare hostname is not covered by an active edge
certificate. Either switch to Flattened hostnames or create an Advanced certificate containing the hierarchical
primary hostname and its wildcard child, then wait until it becomes active.

Total TLS cannot resolve this for Tunnel hostnames because Cloudflare excludes them from Total TLS issuance.

## Turnstile variables

The Variable integration exposes:

| Field | Required | Environment variable |
| --- | --- | --- |
| Site Key | Yes | `CLOUDFLARE_SITE_KEY` |
| Secret Key | Yes | `CLOUDFLARE_SECRET_KEY` |

Attach the integration to an app service or stack to inject these variables. The application must implement and verify
Turnstile; adding the variables does not add a challenge to the app automatically.

## Related pages

- [App access](../apps/access.md)
- [Application Access providers](access.md)
- [Variable integrations](../integrations/variable.md)
