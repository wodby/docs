# Meilisearch

The Wodby Meilisearch catalog stack runs [Meilisearch](https://www.meilisearch.com/), a search engine for websites and
apps, as a single instance. The current services and defaults are documented in
[`wodby/stack-meilisearch`](https://github.com/wodby/stack-meilisearch).

## API keys

Every Meilisearch request except `GET /health` needs an API key, sent as `Authorization: Bearer <key>`.

Wodby generates the master key when the app is created. It is the `master_key` token on the Meilisearch app service's
**Configuration > Tokens** tab, and the `MEILI_MASTER_KEY` variable inside the container. See
[Tokens](../../../apps/tokens.md). Use the master key only to manage API keys, and keep it on your servers. Never put it
in browser code or in a repository.

Meilisearch creates default keys from the master key. List them with the master key:

```bash
curl -H "Authorization: Bearer <master key>" https://<meilisearch domain>/keys
```

- Give browsers and mobile apps the **Default Search API Key**. It can only search.
- Give backends that add or update documents the **Default Admin API Key**, or a narrower key you create with
  `POST /keys`.

See Meilisearch's [security guide](https://www.meilisearch.com/docs/resources/self_hosting/security/basic_security).

Changing the master key changes every key derived from it. The default keys and every key you created stop working, and
your clients need the new keys.

## Connect to Meilisearch

Meilisearch has a public HTTPS domain, so browsers and mobile apps can search it directly. Services in the same app
environment can use `http://<app service name>:7700` instead.

Wodby does not protect the Meilisearch domain with basic auth, and you should not add one under **Endpoints > Auths**.
Meilisearch reads its API key from the `Authorization` header, the same header basic auth uses, so search and indexing
requests would fail. The API keys protect the domain.

Meilisearch accepts document batches of up to 100 MB. The domain allows 5 minutes per request so that large batches can
finish uploading. Do not set the route's request body size: it makes the route hold each request in memory until it is
complete. See [HTTP settings](../../../apps/endpoints.md#http-settings).

## Development and production mode

The mode follows the app environment's [type](../../../apps/environment-types.md):

- In `dev` environments, Meilisearch runs in development mode. Opening the domain in a browser shows Meilisearch's
  search preview, where you can try searches with an API key.
- In `prod`, `staging`, `test`, and `feature` environments, Meilisearch runs in production mode, without the search
  preview.

In both modes, every request except `GET /health` needs an API key.

## Change configuration

Meilisearch settings are `MEILI_*` environment variables on the Meilisearch app service. Change them and deploy the
service. See [Environment variables](../../../apps/environment-variables.md) and Meilisearch's
[configuration reference](https://www.meilisearch.com/docs/resources/self_hosting/configuration/overview).

Index settings, such as searchable, filterable, and sortable attributes, ranking rules, and synonyms, are set per index
through the API.

Meilisearch's telemetry is off.

## Version updates

A Meilisearch database opens only with the version that wrote it. When a stack upgrade brings a newer Meilisearch,
Meilisearch upgrades the database in place when it starts. See [Upgrade](../../../apps/stack.md#upgrade). Searches keep
working during the upgrade, and new tasks wait until it is done. Follow it with `GET /tasks?types=upgradeDatabase`.

Meilisearch warns that this upgrade is not atomic and can, rarely, corrupt the database. Before you upgrade a production
environment, create a dump with `POST /dumps`, or make sure you can reindex from your application's own data. A failed
or stuck upgrade task can be cancelled, which rolls the database back. See Meilisearch's
[update guide](https://www.meilisearch.com/docs/resources/migration/updating).

New non-production environments upgrade their stack automatically by default. Turn
[auto-upgrade](../../../apps/stack.md#auto-upgrade) off for environments whose upgrades you want to control.

## Data and backups

The Meilisearch volume (10 GB by default) holds the database. Dumps and snapshots that you create with the API are
written to the same volume and use its space. Raise the volume size for large datasets.

The Meilisearch service has no backup or import operation in Wodby. Create
[dumps](https://www.meilisearch.com/docs/resources/self_hosting/data_backup/dumps) or snapshots with the API, or keep
the source data in your application so that you can reindex it.

## Limits

- The Meilisearch service is fixed to one replica. It runs one instance on one volume and can't be scaled.
- The stack requests 0.2 CPU and 512 MiB of memory for Meilisearch and limits it to 2 CPU and 2048 MiB. Indexing uses up
  to two thirds of the memory limit, so raise the limit for large indexing batches. Change resources under
  **Runtime > Resources**.
