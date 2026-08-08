# Solr

The Wodby Solr catalog stack runs SolrCloud with a required ZooKeeper service. The current service composition and Solr
version are documented in [`wodby/stack-solr`](https://github.com/wodby/stack-solr).

## Authentication and endpoints

Wodby generates a password for SolrCloud's `solr` administrator account. Applications connected through a stack link
receive the internal hostname and generated credential defined by their service integration.

Solr exposes an HTTP endpoint on port `8983`, so Wodby creates a technical route for its UI and API. Solr already uses
HTTP Basic authentication. Do not add Wodby route-level basic authentication to this route because an HTTP client cannot
send two independent Basic authorization headers.

## Default collection

The Solr post-deployment initialization creates a collection named `default` when the cluster has no collections. It
uses Solr's `_default` configset.

`_default` is only a starting point. Applications that require a particular schema must install their own configset.
For Drupal, follow [Connect Drupal to Solr](../drupal/solr.md) so Search API Solr generates and uploads a compatible
configset.

## Create another collection

You can create collections from the Solr Admin UI. You can also open a [web terminal](../../../apps/web-terminal.md) on
the Solr app service and use the image action:

```bash
make create-collection collection=my_collection num_shards=1 config=_default \
  -f /usr/local/bin/actions.mk
```

Replace `my_collection`, the shard count, and the configset for your application. The command uses the generated
`SOLR_CLOUD_PASSWORD` automatically.

## Configsets

Keep custom configsets in a reproducible application or service workflow and upload them to ZooKeeper. Do not edit
configsets bundled in the running image: those changes are tied to one container and disappear when it is replaced.

When a client integration can generate its own configset, prefer that workflow. After replacing a configset, follow the
client's instructions for reloading the collection and reindexing data.

Use [application backups](../../../apps/backups.md) for supported persistent service data and review volume settings
before production use.
