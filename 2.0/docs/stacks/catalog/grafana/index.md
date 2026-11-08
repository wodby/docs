# Grafana

The Wodby Grafana catalog stack runs Grafana on its own. The current composition and defaults are in
[`wodby/stack-grafana`](https://github.com/wodby/stack-grafana).

## Sign in

Open the Grafana domain listed under **Endpoints** for the app environment. Open the app service's
**Configuration > Tokens** tab and reveal `admin_username` (`admin`) and `admin_password`. See
[Tokens](../../../apps/tokens.md).

Grafana applies these values once, on the first start with an empty data volume. Changing the tokens later does not
change the existing account.

## Add data sources

The stack ships no data sources. The Grafana service can be linked to Grafana Loki, Grafana Tempo, Prometheus, and
VictoriaMetrics services. A link sets no variables and creates no data source by itself.

Declare data sources in the **Grafana datasources** file under **Configuration > Configs**. It is empty by default.
A data source removed from the file is deleted from Grafana on the next start. Grafana reads the file at start, so
deploy the service after a change. See
[Configs tab](../../../apps/services.md#configs-tab).

A linked service is reached at `http://<its app service name>:<its port>`. Loki uses port `3100`, Tempo uses `3200`,
VictoriaMetrics uses `8428`, and Prometheus uses `9090`. To add data sources automatically, use a stack that provisions
them. See the [Prometheus](../prometheus/index.md), [Loki](../loki/index.md), [Tempo](../tempo/index.md), and
[VictoriaMetrics](../victoria-metrics/index.md) guides.

## Change configuration

Add or change `GF_*` [environment variables](../../../apps/environment-variables.md) on the app service, or edit the
data sources file, then deploy. Do not edit `grafana.ini` in the container, because it is not on a volume. Wodby turns
off usage reporting and update checks by default.

## Data

The stack creates a 10 GB **Grafana data** volume, mounted at `/var/lib/grafana`. It holds Grafana's built-in SQLite
database with dashboards, users, and settings, and installed plugins. Wodby defines no backups or imports for this
service. Grafana is not scalable.

## Check that Grafana is running

`/api/health` on port `3000` reports whether Grafana and its database are up.
