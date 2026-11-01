# Elasticsearch

The Wodby Elasticsearch catalog stack runs a single-node Elasticsearch with Kibana. The current services and defaults
are documented in [`wodby/stack-elasticsearch`](https://github.com/wodby/stack-elasticsearch).

## Connect an application

Link your application's app service to the Elasticsearch app service. See [Links](../../../apps/services.md#links-tab).
The app service receives the host, port and password in variables named by the linking service. Read them in code. Do not
copy the password into your repository.

- URL: `http://<app service name>:9200`. Security is on and TLS is off, so use plain `http://` with HTTP Basic
  authentication.
- User: `elastic`, the built-in superuser. Its password is the `password` token on the Elasticsearch app service's
  **Configuration > Tokens** tab.
- Port `9200` is private, and Wodby creates no route for it. Port `9300` is the transport port. Applications do not use
  it.

Wodby also generates a `kibana_password` token for the built-in `kibana_system` user. Kibana uses it. Do not use it from
applications, and do not give Kibana the `elastic` password.

## Sign in to Kibana

Kibana is the main app service, so the app environment's root route opens it. Sign in with user `elastic` and the
Elasticsearch `password` token. `kibana_system` cannot sign in.

The link from Kibana to Elasticsearch is required and is set up by the stack. Kibana stays unready until Elasticsearch is
up. If Kibana reports that the server is not ready, check the Elasticsearch app service first.

Wodby generates three encryption keys for Kibana and keeps them stable across deployments. Replacing them signs users
out and makes encrypted saved objects, such as connector secrets, unreadable.

## Single node and resources

Elasticsearch runs as a single node and does not scale. An index with replicas stays yellow because there is no second
node, so create indices with zero replicas.

The stack requests 1 CPU and 2048 MiB for Elasticsearch and limits it to 2 CPU and 4096 MiB. The JVM heap is fixed at
`-Xms1g -Xmx1g` by default (`ES_JAVA_OPTS`). If you raise the heap, keep the container memory limit above it. Kibana
requests 0.5 CPU and 1024 MiB and is limited to 1 CPU and 2048 MiB. Change resources under **Runtime > Resources**.

## Change configuration

Set Elasticsearch settings as environment variables on its app service, named exactly like the setting, for example
`cluster.name`. Do not mount an `elasticsearch.yml`. See [Environment variables](../../../apps/environment-variables.md).
Turning security off or HTTP TLS on changes how every linked service connects, Kibana included.

Kibana settings are variables in the image's form: the setting name in upper case with dots replaced by underscores. Do
not mount a `kibana.yml`.

## Data and backups

The stack adds a 20 GiB **Elasticsearch data** volume. Kibana has no volume. Dashboards, data views and other saved
objects live in Elasticsearch.

The services have no backup or import support. Snapshots need a repository configured in Elasticsearch itself.

## Check that it works

In a [web terminal](../../../apps/web-terminal.md) on the Elasticsearch app service, run:

```bash
curl -s -u "elastic:$ELASTIC_PASSWORD" http://localhost:9200/_cluster/health?pretty
```
