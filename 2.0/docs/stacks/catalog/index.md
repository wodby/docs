# Catalog stack guides

Catalog stack guides explain application-specific setup that cannot be expressed fully by a stack manifest. Use them
together with the stack and service configuration shown in the dashboard.

The source repository for each stack remains the authoritative reference for its current services, versions, links,
storage, and defaults. Browse all available stacks in the [Wodby stack catalog](https://wodby.com/stacks) or the
[`wodby/stacks`](https://github.com/wodby/stacks) repository.

## Application guides

- [Drupal](drupal/index.md): Wodby runtime configuration, storage, cron, and application actions
- [Connect Drupal to Solr](drupal/solr.md): configure Search API Solr for the catalog Drupal stack
- [WordPress](wordpress/index.md): build, runtime configuration, shared content, and cron behavior
- [Matomo](matomo/index.md): installer database values, geolocation, mail, and archiving cron

## Service stack guides

- [Gotenberg](gotenberg/index.md): private endpoint usage and migration from AthenaPDF
- [Solr](solr/index.md): SolrCloud authentication, collections, and configsets
- [OpenSMTPD](opensmtpd/index.md): outbound relay integrations and test messages
- [FRP Server](frps/index.md): connect external FRPC clients through Wodby routes

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
