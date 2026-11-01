# ZooKeeper

The Wodby ZooKeeper catalog stack runs a ZooKeeper service. The current composition and defaults are in
[`wodby/stack-zookeeper`](https://github.com/wodby/stack-zookeeper).

In Wodby stacks, ZooKeeper is the coordination store of SolrCloud. Applications normally do not talk to it directly.
See the [Solr guide](../solr/index.md).

## Connect a service

Use these values from a service in the same app environment:

- Host: the ZooKeeper app service name
- Client port: `2181`

No client authentication or TLS is configured, and Wodby generates no token. Only the environment's internal network
reaches the service. A linked Solr service uses the host as its `ZK_HOST` and protects its own znodes with digest
credentials.

## Change configuration

On every start, the container builds its `zoo.cfg` from environment variables. With one replica, ZooKeeper runs
standalone. Do not edit the file. Set [environment variables](../../../apps/environment-variables.md) on the app
service instead:

| Variable | Setting | Default |
| --- | --- | --- |
| `ZOO_TICK_TIME`, `ZOO_INIT_LIMIT`, `ZOO_SYNC_LIMIT` | `tickTime`, `initLimit`, `syncLimit` | `2000`, `5`, `2` |
| `ZOO_MAX_CLIENT_CNXNS` | `maxClientCnxns` | `60` |
| `ZOO_AUTOPURGE_PURGE_INTERVAL`, `ZOO_AUTOPURGE_SNAP_RETAIN_COUNT` | Snapshot auto-purge | `0` (off), `3` |
| `ZOO_4LW_COMMANDS_WHITELIST` | Allowed four-letter commands | `stat,ruok,conf,isro` |

## Data

Snapshots are in `/data`, and the transaction log is in `/data/datalog` on the same volume.

The **Data** volume is optional, and the stack does not define one. Without it, data is lost when the container is
replaced. For SolrCloud, that includes the collections' configuration, config sets, and security settings. They live in
ZooKeeper and not on Solr's volume. Wodby defines no backups or imports for this service.

## Check that ZooKeeper is running

Open a [web terminal](../../../apps/web-terminal.md) for the ZooKeeper app service and run:

```bash
echo ruok | nc -w 2 localhost 2181
```

It answers `imok`. `make stat -f /usr/local/bin/actions.mk` prints the server mode and connected clients.
