# Cloudflare

Cloudflare supports two integration types in Wodby:

- `application_access` provides protected publishing through Cloudflare Access or private-network access through
  Cloudflare One
- `variable` injects Cloudflare Turnstile keys into app services or stacks

Create separate integrations when you need both types. Each integration has one selected type and only asks for the
fields required by that use case.

## Application Access

One Cloudflare Application Access integration supports both Wodby access types:

| Wodby access type | Cloudflare path | Address | User experience |
| --- | --- | --- | --- |
| Protected publishing | Public hostname on a managed Tunnel plus a Cloudflare Access application | Hostname in your Cloudflare zone | Users open the public hostname and complete the selected Access policy |
| Private network | Private hostname route on a managed Tunnel | Existing Wodby technical hostname | Enrolled Cloudflare One Client devices connect through WARP; there is no Access login page |

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
6. If you plan to use Protected access, open `Zero Trust > Access controls > Policies` and create at least one reusable
   `Allow` policy. Wodby lists reusable policies; the per-application policy editor is not used for this selection.

The `Cloudflare One Connector: cloudflared` permission covers both managed Tunnels and private hostname routes.

!!! note "One credential for both access types"

    Wodby validates the complete Application Access permission set when the integration is created. Include every
    permission above even if you initially plan to use only Private network access. Private network access does not
    create zone DNS records, an Access application, or an Access policy attachment, but the complete credential keeps
    the same integration usable for either access type.

The integration form asks for the Account ID and API token. Wodby checks authentication and each required permission
when you create the integration, and reports whether the token is invalid or a particular permission is missing. Wodby
does not request certificate permissions.

### Configure an app

Select Protected mode during app creation, or open `Apps > [App] > [Instance] > Settings > Access`. Choose the
Cloudflare Application Access integration, an access type, and whether the scope covers the Entire app or Selected
endpoints.

#### Protected access

Protected access publishes customer-zone hostnames through Cloudflare Tunnel and places a Cloudflare Access login
policy in front of them. Choose:

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

#### Private network access

Private network access makes the selected app endpoints available only to devices connected to your Cloudflare Zero
Trust organization through the Cloudflare One Client. It does not create a Cloudflare Access login page and does not
require a customer DNS zone, Access policy, or hostname input in Wodby.

Before enabling it:

1. Enroll user devices in the
   [Cloudflare One Client](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/).
2. In `Traffic policies > Traffic settings`, enable `Allow Secure Web Gateway to proxy traffic` for TCP. Cloudflare
   also recommends UDP when private DNS resolvers are used.
3. In the WARP device profile, make sure `100.80.0.0/16` and `2606:4700:0cf1:4000::/64` route through WARP. In Exclude
   mode, remove the broader `100.64.0.0/10` exclusion; in Include mode, add the two ranges.
4. In Local Domain Fallback, ensure the Wodby technical-domain suffix is not sent to a local resolver. This lets
   Cloudflare Gateway answer DNS for Wodby's private hostname route.

See Cloudflare's
[private-hostname device connectivity guide](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/private-net/cloudflared/connect-private-hostname/#device-connectivity)
for the current device-profile steps.

Wodby reuses each endpoint's stable technical hostname, creates a private hostname route to the app's managed tunnel,
and serves its existing Wodby-managed HTTPS certificate through the connector. The matching route remains disabled at
Wodby's public gateway. A device outside the configured Cloudflare network therefore cannot use that hostname to reach
the app. The hostname itself is not secret and may still resolve outside WARP; private access comes from the disabled
public route and the Cloudflare One traffic path. Certificate renewals and endpoint changes are reconciled
automatically after deployment.

When access is removed or the app instance is deleted, Wodby removes the connector, tunnel connections, applicable
managed DNS records or private hostname routes, the Tunnel, and the Access application. It does not delete the selected
reusable Access policy, DNS zone, device settings, Gateway policies, or any customer-managed certificate. If a managed
DNS record or private hostname route no longer has Wodby's ownership marker and expected target, Wodby leaves it
untouched and reports a cleanup warning. Temporary API failures are retained as retryable cleanup obligations on the
integration page; keep the integration and its permissions available until cleanup finishes.

Wodby does not use Cloudflare Quick Tunnels or `*.trycloudflare.com` hostnames for either access type. Quick Tunnels
generate random temporary addresses, are intended for testing and development, and have no uptime guarantee. Wodby
instead creates a managed Tunnel: Protected publishing uses hostnames in your selected Cloudflare zone, while Private
network access reuses Wodby technical hostnames. See
[Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/).

### Troubleshooting TLS

For Protected publishing, `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` normally means the selected Cloudflare hostname is not
covered by an active edge certificate. Either switch to Flattened hostnames or create an Advanced certificate
containing the hierarchical primary hostname and its wildcard child, then wait until it becomes active.

Total TLS cannot resolve this for Tunnel hostnames because Cloudflare excludes them from Total TLS issuance.

Private network access does not use a customer-zone Cloudflare edge certificate. The connector presents the existing
Wodby-managed certificate for the technical hostname. If that hostname is unreachable, first confirm that the
Cloudflare One Client is connected, TCP proxying is enabled, the private-hostname IP ranges are routed through WARP,
and Local Domain Fallback does not capture the technical-domain suffix. Then review the app's Access task and status in
Wodby.

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
