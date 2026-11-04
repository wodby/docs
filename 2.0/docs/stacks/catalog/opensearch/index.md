# OpenSearch

The Wodby OpenSearch catalog stack runs a single-node OpenSearch with OpenSearch Dashboards. The current services and
defaults are documented in [`wodby/stack-opensearch`](https://github.com/wodby/stack-opensearch).

## Connect an application

Link your application's app service to the OpenSearch app service. See [Links](../../../apps/services.md#links-tab). The
app service receives the host, port and password in variables named by the linking service. Read them in code. Do not
copy the password into your repository.

- URL: `https://<app service name>:9200`. OpenSearch serves the image's self-signed demo certificate. Your client must
  skip certificate verification or trust that certificate. Plain `http://` requests are refused.
- User: `admin`. Its password is the `password` token on the OpenSearch app service's **Configuration > Tokens** tab.
- All OpenSearch ports are private, and Wodby creates no route for them. Applications use port `9200` only.

The image's other demo accounts have public passwords, so they are removed each time the node starts. The `kibanaserver`
account remains for Dashboards, with its own generated `dashboards_password` token. Create your own users through the
security API instead of reusing these names.

## Sign in to Dashboards

OpenSearch Dashboards is the main app service, and it has a public HTTPS address. Sign in as `admin` with the OpenSearch
`password` token. Create other users under **Security** in Dashboards.

The address accepts sign-ins from anywhere. Do not turn on Wodby Basic Auth for it, because Dashboards reads the
`Authorization` header for its own login. To restrict who can reach the address, use
[Private App Access](../../../apps/access.md).

The Dashboards version must match the OpenSearch version in major and minor. Wodby generates a `cookie_password` token
once to encrypt session cookies. Replacing it signs users out.

## Single node and resources

OpenSearch runs as a single node and does not scale. An index with replicas stays yellow because there is no second node,
so create indices with zero replicas.

The stack requests 1 CPU and 2048 MiB for OpenSearch and limits it to 2 CPU and 4096 MiB. The JVM heap is fixed at
`-Xms1g -Xmx1g` by default (`OPENSEARCH_JAVA_OPTS`). If you raise the heap, keep the container memory limit above it.
Dashboards requests 0.5 CPU and 1024 MiB and is limited to 1 CPU and 2048 MiB. Change resources under
**Runtime > Resources**.

## Change configuration

Set OpenSearch settings as environment variables on its app service, named exactly like the setting, for example
`cluster.name`. Do not mount an `opensearch.yml`. See [Environment variables](../../../apps/environment-variables.md).
Disabling the security plugin changes the scheme to `http://` and removes authentication for every linked service.

Dashboards has a config file, `opensearch_dashboards.yml`, that you can override under **Configuration > Configs**. Keep
`opensearch_security.cookie.secure: true`, because the public address always uses HTTPS. Environment variables set by the
link take precedence over the same settings in the file.

## Data and backups

The stack adds a 20 GiB **OpenSearch data** volume. Dashboards has no volume. Dashboards, index patterns and other saved
objects live in OpenSearch.

The services have no backup or import support. Snapshots need a repository configured in OpenSearch itself.

## Check that it works

In a [web terminal](../../../apps/web-terminal.md) on the OpenSearch app service, run:

```bash
curl -sk -u "admin:$OPENSEARCH_INITIAL_ADMIN_PASSWORD" https://localhost:9200/_cluster/health?pretty
```
