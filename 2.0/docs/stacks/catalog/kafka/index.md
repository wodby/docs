# Apache Kafka

The Wodby Apache Kafka catalog stack runs a single Apache Kafka node. The current composition and defaults are in
[`wodby/stack-kafka`](https://github.com/wodby/stack-kafka).

## What the stack runs

The node runs in KRaft mode and acts as both broker and controller. There is no ZooKeeper service, and the service
cannot be scaled to more than one node. Do not pair it with the [ZooKeeper](../zookeeper/index.md) stack.

Wodby generates the cluster ID once. The internal offsets and transaction topics use a replication factor of `1`, so a
topic that needs a replication factor above `1` cannot be created.

## Connect an application

Use these values from a service in the same app environment:

- Bootstrap server: `<app service name>:9092`
- Security protocol: `PLAINTEXT`

The broker has no TLS, no username, no password, and no certificate. The port is private, so Wodby creates no public
route for it. The broker advertises the app service name as its address, so a client must be able to resolve that name.
This works for services in the same environment.

A service linked to Kafka receives the host and port in variables named by the linking service. Read those variables
instead of hardcoding the host.

## Change broker settings

Set broker properties as [environment variables](../../../apps/environment-variables.md) on the Kafka app service. Use
the `KAFKA_*` form: a broker property in upper case with dots replaced by underscores. Do not mount a `server.properties`
file.

Do not change the listener, advertised listener, node ID, or controller quorum variables. Doing so breaks the
single-node setup.

## Data

Log segments and cluster metadata are stored on the **Kafka data** volume. The stack creates it with a size of 20 GB.
Wodby defines no backups or imports for this service.

## Check that the broker is running

Open a [web terminal](../../../apps/web-terminal.md) for the Kafka app service and run:

```bash
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

`/opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092` also answers when the broker is up.
