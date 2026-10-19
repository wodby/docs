# Cloudflare

Cloudflare exposes five integration kinds in Wodby:

- **API** (`variable`) injects an Account ID and API token into compatible app services or stacks.
- **SMTP (Beta)** (`smtp`) relays transactional email through Cloudflare Email Service.
- **Application Access** (`application_access`) provides protected publishing through Cloudflare Access or
  private-network access through Cloudflare One.
- **R2** (`storage`) stores app and database backups in customer-owned Cloudflare R2 buckets.
- **Turnstile** (`variable`) injects Cloudflare Turnstile keys into app services or stacks.

Select any combination of kinds when creating the integration. Wodby asks only for fields belonging to the selected
kinds. You can also create separate integrations when the credentials should have different owners, sharing, or
permission scope.

## API

Create a Cloudflare integration with the **API** kind when application code needs to call Cloudflare APIs directly.
The kind exposes:

| Field      | Required | Environment variable     |
| ---------- | -------- | ------------------------ |
| Account ID | Yes      | `CLOUDFLARE_ACCOUNT_ID`  |
| API Token  | Yes      | `CLOUDFLARE_API_TOKEN`   |

Create a token with the permissions and resource scope required by the consuming application. The API and Application
Access kinds use the same Account ID and API token fields, so selecting both asks for those credentials only once.
Turnstile widget keys are created separately and are not Cloudflare API credentials.

## Certificate validation behind Cloudflare

This section applies to a custom public domain proxied through Cloudflare when Wodby manages its Let's Encrypt
certificate. It also applies when you configured Cloudflare outside Wodby and have no Cloudflare integration in Wodby.

Cloudflare's visitor-facing certificate and the certificate served by your Wodby origin have separate renewal flows.
Cloudflare's automatic validation exceptions apply to certificates it manages and recognized validation tokens; they
do not provide a blanket exemption for Wodby's origin-certificate renewal. See the
[Cloudflare WAF FAQ](https://developers.cloudflare.com/waf/troubleshooting/faq/#why-are-some-rules-bypassed-when-i-did-not-create-an-exception).

### Identify a browser challenge

A response with `cf-mitigated: challenge` means Cloudflare returned a browser verification page instead of the expected
response. Wodby's automated verification cannot complete that JavaScript/cookie challenge. A `403` or
`Server: cloudflare` header alone is not proof that Cloudflare denied the request: the origin can return a `403` through
Cloudflare too. See [Cloudflare's response marker](https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/detect-response/).

If a renewal notification or task log identifies a Cloudflare challenge, use its observation time and Ray ID to find
the request in [Cloudflare Security Events](https://developers.cloudflare.com/waf/analytics/security-events/). Filter by
the affected hostname and `/.well-known/acme-challenge/` path. Record the rule or security feature that issued the
challenge before changing settings. A missing event alone does not rule out Cloudflare; event availability depends on
the product and logging.

### Allow certificate validation

1. Ask the person managing the Cloudflare zone to review the matching event.
2. Exclude the affected hostname's ACME validation path from the rule issuing the browser challenge. For example, this
   expression matches only validation requests for `example.com`:

   ```text
   (http.host eq "example.com" and starts_with(http.request.uri.path, "/.well-known/acme-challenge/"))
   ```

3. If using a WAF **Skip** rule, place it before the relevant challenge rule and select the applicable skip options.
   Skip only the protections causing the validation failure. A Skip action is not a universal bypass of every
   Cloudflare security product. See [Skip rules](https://developers.cloudflare.com/waf/custom-rules/skip/) and
   [available options](https://developers.cloudflare.com/waf/custom-rules/skip/options/).
4. Confirm that redirects, Workers, and cache rules forward the challenge to the correct origin and preserve its
   response. A successful validation response is `200` with the exact token proof, not an HTML page.
5. Allow Wodby's next scheduled renewal attempt or contact support to verify a retry. Keep protection enabled for the
   rest of the website.

!!! note "Bot Fight Mode has different controls"

    Standard Bot Fight Mode cannot be skipped with WAF custom rules or Page Rules. If the event identifies that
    feature, review Cloudflare's [false-positive guidance](https://developers.cloudflare.com/bots/troubleshooting/false-positives/)
    with the zone administrator to choose a configuration that permits automated validation. Adding a WAF Skip rule
    alone will not resolve it.

Allowing only traffic recognized as a certificate-authority bot is insufficient: Wodby also probes the challenge before
submitting it for validation. Testing from your own browser can succeed while the automated request is challenged.

For other errors and retry behavior, see [certificate troubleshooting](../apps/certificate-troubleshooting.md). For
Cloudflare Tunnel hostnames created through Application Access, use the certificate requirements in
[Protected access](#protected-access); the public origin HTTP validation steps above describe a different certificate
path.

## SMTP

Cloudflare Email Service SMTP submission is currently in beta. Before creating the integration:

1. Enable Email Sending for the Cloudflare account.
2. Onboard the sender domain under **Email Service > Email Sending**.
3. Create an account-owned or user-owned API token with **Email Sending: Edit** for that account.

The SMTP kind asks for one field:

| Field | Required | Stored variable |
| --- | --- | --- |
| Email Sending API Token | Yes | `CLOUDFLARE_API_TOKEN` |

Wodby resolves the token to this fixed relay configuration:

| Setting | Value |
| --- | --- |
| Host | `smtp.mx.cloudflare.net` |
| Port | `465` |
| Security | Implicit TLS (`smtps`) |
| Username | `api_token` |
| Password | The Email Sending API token |

Cloudflare does not support outbound submission on port `587` with STARTTLS. The sender address must use a domain
onboarded for Email Sending in the account that owns the token.

The API and SMTP kinds reuse the same `api_token` field. Select both kinds when the application also sends through the
Cloudflare REST API; Wodby additionally asks for the Account ID and exposes `CLOUDFLARE_ACCOUNT_ID` with
`CLOUDFLARE_API_TOKEN`. The token must have every permission needed by the selected use cases.

See [Cloudflare Email Service SMTP](https://developers.cloudflare.com/email-service/api/send-emails/smtp/) and the
[Email Sending REST API](https://developers.cloudflare.com/email-service/api/send-emails/rest-api/).

## R2

Create a Cloudflare integration with the **R2** kind when you want Wodby to store app or database backups in your own
Cloudflare R2 bucket.

This is a customer-owned third-party backup destination. It is separate from
[Wodby Blob Storage](wodby-blob-storage.md), which does not expose or require customer bucket credentials.

### Before creating the integration

1. Copy the 32-character `Account ID` from the Cloudflare dashboard. See
   [Find account and zone IDs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/).
2. Open `R2 Object Storage > Manage API Tokens` and create an R2 API token with **Object Read & Write** permission.
3. Restrict the token to the buckets Wodby may use.
4. Copy the token's `Access Key ID` and `Secret Access Key`. See
   [R2 API tokens](https://developers.cloudflare.com/r2/api/s3/tokens/).

**Object Read & Write** is sufficient when you enter the exact bucket name manually. To populate the bucket selector
with existing buckets instead, create an account-wide token with **Admin Read & Write** permission. Bucket listing is
optional and does not need to be added to a bucket-scoped token.

The integration form requires:

| Field | Required |
| --- | --- |
| Account ID | Yes |
| Access Key ID | Yes |
| Secret Access Key | Yes |

When you save the integration, Wodby validates the Account ID and credentials against R2's S3-compatible API. If the
token cannot list buckets, enter the exact bucket name when creating a backup or backup preset. Wodby validates access
to that destination separately. The credentials must allow object reads and writes in every bucket used as a backup
destination, including deleting backup objects during cleanup.

When creating a backup or backup preset, select the Cloudflare R2 integration and then select or enter its destination bucket.
Wodby uploads, restores, and downloads backup objects through R2's S3-compatible API. Download and restore operations
use expiring provider-signed URLs.

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
3. Under `Permissions`, add the Account permission `Cloudflare One Connector: cloudflared`: Edit. This shared
   permission is required for both access modes.
4. Under `Account Resources`, include the intended Cloudflare account.
5. For Protected access, add the Account permissions `Access: Apps`: Edit and `Access: Policies`: Edit, then add the
   Zone permissions `Zone`: Read and `DNS`: Edit. Under `Zone Resources`, include only the zones Wodby may publish.
6. For Protected access, open `Zero Trust > Access controls > Policies` and create at least one reusable `Allow`
   policy. Wodby lists reusable policies; the per-application policy editor is not used for this selection.
7. For Private network access, add the Account permission `Cloudflare One Networks`: Edit. No Zone, DNS, or Access
   policy permission is required for this mode.

The `Cloudflare One Connector: cloudflared` permission covers both managed Tunnels and private hostname routes.

!!! note "Grant only the permissions you need"

    Saving the integration validates the API token and the shared cloudflared connector access. Missing permissions
    for an access mode you did not configure are reported as a notice and do not block the integration. When you
    create an app, Wodby validates every permission required by the selected mode and prevents app creation if the
    token or resource scope is insufficient.

The integration form asks for the Account ID and API token. When you save it, Wodby checks authentication and the
shared cloudflared connector permission. The integration page reports mode-specific readiness notices; the selected
mode's full permission check runs when you create an app. Wodby does not request certificate permissions.

### Configure an app

Select Protected mode during app creation, or open `Apps > [App] > [Environment] > Settings > Access`. Choose the
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
2. In `Traffic policies > Traffic settings`, enable `Allow Secure Web Gateway to proxy traffic` and select both TCP
   and UDP. TCP carries the HTTPS connection to the app. UDP is required for the private DNS query that resolves the
   hostname through the managed Tunnel connector.
3. In the WARP device profile, make sure `100.80.0.0/16` and `2606:4700:0cf1:4000::/64` route through WARP. In Exclude
   mode, remove the broader `100.64.0.0/10` exclusion. You can add back exclusions for unused CGNAT ranges, but
   `100.80.0.0/16` must continue to route through WARP. In Include mode, add both required ranges.
4. In Local Domain Fallback, ensure the Wodby technical-domain suffix is not sent to a local resolver. This lets
   Cloudflare Gateway answer DNS for Wodby's private hostname route.

See Cloudflare's
[private-hostname device connectivity guide](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/private-net/cloudflared/connect-private-hostname/#device-connectivity)
for the current device-profile steps.

These are connectivity requirements, not optional Gateway inspection settings. Without UDP proxying, the private
hostname may return `NXDOMAIN`. Without TCP proxying or the required Split Tunnel routes, DNS may succeed but the HTTPS
connection will not reach the managed Tunnel.

Wodby reuses each endpoint's stable technical hostname, creates a private hostname route to the app's managed tunnel,
and serves its existing Wodby-managed HTTPS certificate through the connector. The matching route remains disabled at
Wodby's public gateway. A device outside the configured Cloudflare network therefore cannot use that hostname to reach
the app. The hostname itself is not secret and may still resolve outside WARP; private access comes from the disabled
public route and the Cloudflare One traffic path. Certificate renewals and endpoint changes are reconciled
automatically after deployment.

!!! note "HTTP endpoints only"
    The Gateway TCP proxy setting above lets the Cloudflare One Client carry the HTTPS connection to Wodby's private
    hostname route. It does not expose arbitrary app TCP or UDP ports through Application Access. Entire app scope
    prevents public port publishing; with Selected endpoints scope, separately published TCP or UDP ports remain
    public and outside Cloudflare Application Access.

When access is removed or the app environment is deleted, Wodby removes the connector, tunnel connections, applicable
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

## Turnstile

Create a Cloudflare integration with the **Turnstile** kind selected, then copy the site and secret keys from the
corresponding widget in the Cloudflare dashboard. The kind exposes:

| Field      | Required | Environment variable   |
| ---------- | -------- | ---------------------- |
| Site Key   | Yes      | `TURNSTILE_SITE_KEY`   |
| Secret Key | Yes      | `TURNSTILE_SECRET_KEY` |

Attach the integration to an app service or stack that supports the Cloudflare Turnstile kind. Wodby injects only the
Turnstile fields for that service requirement; fields from a separately selected Application Access kind are not
included. The application must implement and verify Turnstile—attaching the integration does not add a challenge to
the app automatically.

## Related pages

- [Storage providers](storage.md)
- [SMTP providers](smtp.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
- [App access](../apps/access.md)
- [Application Access providers](access.md)
- [Variable integrations](../integrations/variable.md)
