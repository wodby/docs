# Valkey

The Wodby Valkey catalog stack runs a single Valkey service. The current composition and defaults are documented in
[`wodby/stack-valkey`](https://github.com/wodby/stack-valkey).

## Connect an application

The Valkey service listens on port `6379` and speaks the Redis protocol, so Redis clients work unchanged. The service has
no HTTP endpoint, so Wodby creates no route for it.

1. Link your application's app service to the Valkey app service. See [Links](../../../apps/services.md#links-tab).
2. Read the connection values from the environment variables your app service receives. The linking service chooses
   their names. They usually keep the Redis prefix, for example `REDIS_HOST`, `REDIS_PORT` and `REDIS_PASSWORD`, or a single
   `REDIS_URL`.

A password is always required. Wodby generates it as the `password` token. Open the Valkey app service's
**Configuration > Tokens** tab to see it. Do not hardcode the host or copy the password into your repository.

## Choose cache or storage behavior

With the defaults, Valkey is a cache. It holds up to 128 MB (`VALKEY_MAXMEMORY`). After that it evicts any key, including
keys without an expiry (`VALKEY_MAXMEMORY_POLICY` is `allkeys-lru`).

If you store a job queue, sessions or other data that must not disappear, set `VALKEY_MAXMEMORY_POLICY` to `noeviction`
and raise `VALKEY_MAXMEMORY`. Otherwise Valkey drops data silently under memory pressure.

Set these variables on the Valkey app service under **Configuration > Variables**. See
[Environment variables](../../../apps/environment-variables.md). They apply on the next deployment. Do not edit the
generated configuration file; it is rewritten on every start.

| Variable | Effect | Default |
| --- | --- | --- |
| `VALKEY_MAXMEMORY` | Memory limit | `128m` |
| `VALKEY_MAXMEMORY_POLICY` | Eviction policy | `allkeys-lru` |
| `VALKEY_DATABASES` | Number of databases | `16` |
| `VALKEY_TIMEOUT` | Idle client timeout, in seconds | `300` |
| `VALKEY_NOTIFY_KEYSPACE_EVENTS` | Keyspace notifications | empty |

## Data and backups

The stack does not add the optional **Data** volume. Without it nothing is written to disk, and every restart or
deployment starts with an empty Valkey. To keep data, add the volume under **Runtime > Volumes** on the Valkey app
service and redeploy. Wodby then turns persistence on. Once added, the volume cannot be resized or removed. See
[Volumes](../../../apps/services.md#volumes-tab).

The service has no backup or import support.

## Check that it works

Open a [web terminal](../../../apps/web-terminal.md) on the Valkey app service and run:

```bash
valkey-cli -a "$VALKEY_PASSWORD" ping
```

The answer is `PONG`. Use `config get maxmemory-policy` and `config get appendonly` to see the eviction policy and whether
persistence is on. `info stats` shows `evicted_keys`.
