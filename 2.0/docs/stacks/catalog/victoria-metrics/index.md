# VictoriaMetrics

The Wodby VictoriaMetrics catalog stack runs single-node VictoriaMetrics with Grafana as its interface. The current
composition and defaults are in [`wodby/stack-victoria-metrics`](https://github.com/wodby/stack-victoria-metrics).

## Choose services when you create the app

VictoriaMetrics is required. Grafana is enabled by default and is the stack's public interface. Its VictoriaMetrics
data source is provisioned for you.

## Sign in to Grafana

Open the Grafana app service's **Configuration > Tokens** tab and reveal `admin_username` (`admin`) and
`admin_password`. Grafana applies them once, on the first start with an empty data volume. Changing the tokens later does
not change the existing account. See [Tokens](../../../apps/tokens.md) and the [Grafana guide](../grafana/index.md).

## Send and query metrics

VictoriaMetrics listens on port `8428`. The port is private, so Wodby creates no public route for it. Other services in
the app environment reach it at `http://<VictoriaMetrics app service name>:8428`. No authentication is configured.

The same port serves:

- the Prometheus-compatible query API (`/api/v1/query`, `/api/v1/query_range`), which Grafana uses
- Prometheus remote write (`/api/v1/write`)
- the built-in interface (`/vmui`)

Wodby sets no scrape configuration. Metrics arrive only when something writes them.

## Limits

- Retention is the upstream default. Wodby sets none.
- VictoriaMetrics has no settings, links, or config files in Wodby. Environment variables are not read as flags, so you
  cannot change its flags this way.
- It is not scalable.

## Data

The stack creates a 20 GB **VictoriaMetrics data** volume, mounted at `/victoria-metrics-data`. Grafana has its own
10 GB volume. Wodby defines no backups or imports for these services.

## Check that it is ready

`/-/ready` and `/-/healthy` on port `8428` are the readiness and liveness endpoints.
