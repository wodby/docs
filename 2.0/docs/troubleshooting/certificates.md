# Certificate issuance and renewal

Use this guide when a Let's Encrypt certificate task fails, a custom domain remains pending, or an automatic renewal
does not complete. Start with the failed [task's logs](../tasks.md) and the expiry shown under
`Organization > Certificates`.

A failed renewal does not immediately invalidate the existing certificate. It remains usable until its expiry date.
Resolve the cause before that date; repeated attempts alone cannot fix a blocked validation request.

## Check how the domain is validated

- **Custom public domains:** Wodby temporarily serves a verification response at
  `http://example.com/.well-known/acme-challenge/<token>`. Requests must reach that response through every proxy and
  routing layer in front of the app.
- **Wodby technical domains:** Wodby manages DNS validation. HTTP browser challenges on the app's pages do not explain
  a DNS-validation failure. Use the task's reported DNS or certificate-authority error when contacting support.
- **Uploaded custom certificates:** These are not renewed automatically. Obtain and upload a replacement before expiry.

See [TLS certificates](../apps/endpoints.md#tls-certificates) for certificate ownership and domain setup.

## Interpret the failure

| Message or response | What to check |
| --- | --- |
| Domain did not resolve, `Awaiting DNS`, or DNS lookup failed | Verify the hostname's public DNS records, including any IPv6 records. A DNS timeout can also indicate a temporary resolver problem. |
| `401` or `403` | Authentication, a firewall rule, a browser challenge, or the application may have denied the request. The status alone does not identify the responsible component. |
| Cloudflare browser verification challenge | Follow the [Cloudflare certificate troubleshooting steps](../providers/cloudflare.md#certificate-validation-behind-cloudflare). Automated validation cannot complete a JavaScript or cookie challenge. |
| `404` or `200` with an unexpected response body | The request may have reached the application, another origin, or a cached response instead of the temporary solver. Check hostname, path routing, redirects, and cache rules. |
| Connection refused, host unreachable, or probe timeout | Check public HTTP reachability, proxy origin settings, and cluster health. Read earlier probe messages too: a final timeout may follow repeated HTTP errors. |
| Let's Encrypt rate limit or temporary service error | Follow the retry time in the notification. Repeated manual retries can prolong a rate-limit problem. |

## Check the active challenge path

1. Use the exact hostname and challenge path from the current task log. The token changes between attempts.
2. Ensure requests can start on port 80. An HTTP-to-HTTPS redirect can work if its destination still serves the correct
   verification response. A login page, browser challenge, application page, or redirect to another site cannot replace it.
   See [Let's Encrypt's HTTP-01 requirements](https://letsencrypt.org/docs/challenge-types/#http-01-challenge).
3. Check proxy routing and security logs at the failure's UTC timestamp. Keep the exact validation path out of browser
   authentication and response rewriting, and avoid caching temporary challenge responses.
4. Test while the solver is running. Wodby removes temporary solver resources after the attempt, so a later `404` on an
   old token does not prove that the solver failed during renewal.

A successful browser request from your computer does not prove that the renewal worker or certificate authority can
reach the same response. Security products may treat requests differently by source network or client characteristics.
If results differ, share the task link, hostname, UTC time, and any proxy request identifier with support.

## Retry and recovery

Failed renewal attempts are retried after increasing delays of one through seven days, then weekly. A longer delay
requested by the certificate authority takes precedence. Each failed attempt sends an email with the next scheduled
retry time, and the task log records it too. If backoff would cross expiry, Wodby schedules one additional attempt at
expiry, subject to the certificate authority's retry delay and app/cluster availability. See [renewal notifications](../user/notifications.md#certificate-renewal-notifications).

After correcting the cause:

- For a new domain that is still pending, select `Reconcile certificate` on the route to check it again, as described
  under [custom domains](../apps/endpoints.md#tls-certificates).
- For an existing certificate, allow the next scheduled renewal attempt shown in the failure notification, or contact
  support to verify a retry.
- Check that the certificate expiry advances after renewal. Automatic renewal sends a recovery notification after a
  successful retry following failures, subject to your [notification preferences](../user/notifications.md).

If expiry is close or the next attempt still fails, contact [Wodby support](../support.md) with the task link and relevant
diagnostics. Do not include private keys, API tokens, or browser cookies.
