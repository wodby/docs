# Prometheus

The Wodby Prometheus catalog stack runs Prometheus and an optional Grafana service. The current composition and defaults
are in [`wodby/stack-prometheus`](https://github.com/wodby/stack-prometheus).

## Choose services when you create the app

Prometheus is the stack's main service. Grafana is enabled by default and can be excluded when you create the app.
Wodby provisions a Prometheus data source in Grafana for you, and the Prometheus service is linked to it. Apps created
before Grafana became a default keep their choice; enable the Grafana app service there to add it.

## Open Prometheus

Prometheus listens on port `9090`. Wodby protects the service's public domains with basic auth by default. Each app
service gets its own generated password. Reveal it under **Endpoints > Auths** for the app environment. See
[Auths](../../../apps/endpoints.md#auths).

## Change the Prometheus configuration

The **Prometheus config** file is available under the app service's **Configuration > Configs** tab. Its default comes
from the service image. An app override replaces the default, and **Reset override** restores the image's file on the
next deployment. See [Configs tab](../../../apps/services.md#configs-tab).

## Sign in to Grafana

When Grafana is enabled, open the Grafana app service's **Configuration > Tokens** tab and reveal `admin_username`
(`admin`) and `admin_password`. Grafana applies them once, on the first start with an empty data volume. Changing the
tokens later does not change the existing account. See [Tokens](../../../apps/tokens.md).

The Prometheus data source is the default. It is defined in Grafana's **Grafana datasources** config file. A data source
removed from that file is deleted from Grafana on the next start. See the [Grafana guide](../grafana/index.md).

## Data

The stack creates a 10 GB **Data** volume for Prometheus. Grafana, when enabled, has its own 10 GB volume with its
dashboards, users, settings, and plugins. Wodby defines no backups or imports for Grafana.

Prometheus is not scalable.
