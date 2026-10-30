# Uptime checks

Wodby requests your custom domains once a minute from outside Wodby, from more than one location. If a domain stops
answering, Wodby records a task on the app environment and emails your organization admins. It does the same when the
domain comes back.

Uptime checks are available on paid plans. You don't need to set anything up: a check starts automatically once a
domain has resolved.

- A domain with a Let's Encrypt certificate starts after the certificate is issued.
- Any other domain starts once its hostname resolves to a public address.

If your organization moves to the free Developer plan, its checks stop.

## What is checked

Each hostname has one check, shared by all of its paths. The check sends a `GET` request to the hostname's main or
primary path, or otherwise to its shortest path. It uses HTTPS when the domain has a certificate and HTTP when it
doesn't.

These aren't checked:

- Wodby-generated [technical domains](endpoints.md#technical-domains)
- private routes
- wildcard hostnames
- domains that [Application Access](access.md) publishes through a provider

## What counts as down

A check fails when:

- the hostname doesn't resolve, or resolves to a private address
- the connection fails
- the TLS certificate can't be verified, for example because it expired or doesn't cover the hostname
- the domain doesn't answer within 10 seconds
- the response is a `5xx` status

A domain counts as down when this happens in two checks in a row and a second location agrees. A short network problem
or a single failed request doesn't cause an alert.

A domain must pass once before it can alert. A domain that has never answered, such as an old hostname that no longer
points to your app, doesn't send any alerts.

A domain counts as up again after two passing checks in a row.

Every other response counts as up, including redirects, `401`, `403`, `404`, and `429`. A check shows that something
answers, not that your app works correctly:

- A site behind Basic Auth answers `401`, so the check only shows that something answers.
- Wodby doesn't follow redirects, so a redirect counts as up even if its destination is down.
- A domain behind a proxy or CDN may answer from the proxy while your app is down.

### Deployments and maintenance mode

Checks keep running during deployments. A deployment that makes a domain fail two checks in a row is reported as an
outage.

[Maintenance mode](maintenance.md) responds with `503`, so a domain in maintenance mode is reported as down. To avoid
this during planned maintenance, turn off the domain's check first.

## Outage and recovery alerts

Each outage and recovery appears as an automatic task on the app environment, with a title such as
`Domain example.com is down` or `Domain example.com recovered`. You can find these tasks in the app's
[task list](tasks.md). The down task's log shows why the check failed.

Wodby also emails organization admins about each outage and recovery. Each admin can turn these emails off for
themselves with the `Custom domain outages and recoveries` setting in their
[notification settings](../user/notifications.md#custom-domain-outage-notifications). Tasks are recorded either way.

A domain that keeps going down and coming back sends at most one down email per 30 minutes. If an outage ends before
its down email is due, Wodby sends no email about it. You only get a recovery email for an outage you were emailed
about.

## Domains down for 7 days

After a domain has been down for 7 days, Wodby checks it once an hour and sends admins one email about it. If the
domain no longer points to Wodby, turn off its check or remove the domain.

If the domain comes back, one passing check ends the outage, Wodby emails admins, and checks return to once a minute.

## When checks don't run

Checks don't run while an app environment is paused, or while it is being created, imported, paused, resumed, migrated,
or deleted.

These actions end an open outage without a recovery email:

- turning off the domain's check
- disabling the domain's routes
- pausing the app environment

## Turn a check off

Checks are on by default. To turn one off, open the domain from `Apps > [App] > [Environment] > Endpoints > Domains`
and turn off its uptime check. The change applies to every path of that hostname.

You can also use the API: send `PUT /v1/app-routes/{id}/uptime-check` with `{"enabled": false}`.

Turning a check back on requires a paid plan. The domain must pass once again before it can alert.

## Requests in your logs

Each checked domain gets one request a minute in your access logs, with a user agent that starts with
`WodbyUptimeCheck/1.0`. A domain that is failing can get a few more, because other locations confirm the failure.

These requests count as normal traffic for your app and [rate limits](endpoints.md#request-rate-limits). To leave them
out of your analytics, filter by the user agent.

The requests come from changing IP addresses, so you can't allowlist them by IP. If a firewall drops requests from
addresses it doesn't know, the check fails and the domain is reported as down. In that case, turn off the domain's
check.

Don't use the user agent to grant access. Anyone can send the same value.
