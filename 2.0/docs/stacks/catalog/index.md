# Catalog stack guides

Every stack in the catalog has a guide here. Guides explain what to set when creating an environment, how to sign in
or connect, and what to back up. Use them together with the stack and service configuration shown in the dashboard.

The source repository for each stack remains the authoritative reference for its current services, versions, links,
storage, and defaults. Browse all available stacks in the [Wodby stack catalog](https://wodby.com/stacks) or the
[`wodby/stacks`](https://github.com/wodby/stacks) repository.

## Application stacks

[Drupal](drupal/index.md) ([connect to Solr](drupal/solr.md)), [WordPress](wordpress/index.md),
[Ghost](ghost/index.md), [Matomo](matomo/index.md), [Discourse](discourse/index.md), [Chatwoot](chatwoot/index.md),
[Mattermost](mattermost/index.md), [Dagster](dagster/index.md), [Slack Inviter](slack-inviter/index.md)

## Framework stacks

[HTML](html/index.md), [Angular](angular/index.md), [React](react/index.md), [Vue](vue/index.md),
[PHP](php/index.md), [Laravel](laravel/index.md), [Python](python/index.md), [Django](django/index.md),
[FastAPI](fastapi/index.md), [Flask](flask/index.md), [Ruby](ruby/index.md), [Rails](rails/index.md),
[Go](go/index.md), [Node.js](node/index.md), [Next.js](nextjs/index.md)

## Backend platforms

[Supabase](supabase/index.md)

## Databases

[MariaDB](mariadb/index.md), [MySQL](mysql/index.md), [PostgreSQL](postgres/index.md), [PostGIS](postgis/index.md),
[Cloud MySQL](cloud-mysql/index.md), [Cloud MariaDB](cloud-mariadb/index.md),
[Cloud PostgreSQL](cloud-postgres/index.md)

## Data, messaging and search

[Valkey](valkey/index.md), [Redis](redis/index.md), [Memcached](memcached/index.md), [RabbitMQ](rabbitmq/index.md),
[Distribution Registry](distribution/index.md), [Solr](solr/index.md), [Elasticsearch](elasticsearch/index.md),
[OpenSearch](opensearch/index.md), [ClickHouse](clickhouse/index.md), [Apache Kafka](kafka/index.md),
[Apache Spark](spark/index.md), [Apache Airflow](airflow/index.md), [ZooKeeper](zookeeper/index.md)

## Utilities and integrations

[Mailpit](mailpit/index.md), [OpenSMTPD](opensmtpd/index.md), [Gotenberg](gotenberg/index.md),
[Tailscale](tailscale/index.md), [3X UI](3xui/index.md), [FRP Server](frps/index.md), [OpenClaw](openclaw/index.md)

## Identity and access

[Keycloak](keycloak/index.md)

## AI inference

[vLLM](vllm/index.md)

## Observability

[Prometheus](prometheus/index.md), [Grafana](grafana/index.md), [Grafana Loki](loki/index.md),
[VictoriaMetrics](victoria-metrics/index.md)

## Kubernetes system stacks

[Kubernetes system stacks](system/index.md) are deployed by Wodby to operate a cluster.

## Shared operations

Common application operations are documented once in the shared product documentation:

- use [database details](../../databases/index.md) for MariaDB and PostgreSQL connection metadata
- use [published ports](../../apps/endpoints.md#publishing-ports) for external database, Redis, and other non-HTTP access
- use the [web terminal](../../apps/web-terminal.md) for interactive access to running containers
- use [imports](../../apps/imports.md), [backups](../../apps/backups.md), and [cron schedules](../../apps/cron.md) for
  application operations
- use [SMTP providers](../../providers/smtp.md) for reusable outbound mail credentials

Version histories are not duplicated here. See releases and tags in the corresponding stack and service source
repositories.
