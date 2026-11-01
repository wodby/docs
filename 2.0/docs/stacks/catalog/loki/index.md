# Grafana Loki

The Wodby Grafana Loki catalog stack runs Loki with Grafana as its interface. The current composition and defaults are
in [`wodby/stack-loki`](https://github.com/wodby/stack-loki).

## Choose services when you create the app

Loki is required. Grafana is enabled by default as the stack's main interface, with Loki provisioned as its default
data source. You can exclude Grafana when you need only the Loki API.

## Sign in to Grafana

Open the Grafana app service's **Configuration > Tokens** tab and reveal `admin_username` (`admin`) and
`admin_password`. Grafana applies them once, on the first start with an empty data volume. Changing the tokens later does
not change the existing account. See [Tokens](../../../apps/tokens.md) and the [Grafana guide](../grafana/index.md).

## Connect to Loki

Loki runs as a single instance and listens on port `3100`. The port is private, so Wodby creates no public route for
it. Other services in the app environment reach it at `http://<Loki app service name>:3100`.

Authentication is off, and Loki stores chunks, index, and rules on the local filesystem.

## Data

The stack creates a 20 GB **Loki data** volume, mounted at `/loki`. Grafana has its own 10 GB volume. Wodby defines no
backups or imports for these services.

## Limits

- Loki has no settings, links, or config files in Wodby. Its configuration file is part of the image and is not on a
  volume, so do not edit it in the container.
- Loki is not scalable.

## Check that Loki is ready

`/ready` on port `3100` answers when Loki can accept requests.
