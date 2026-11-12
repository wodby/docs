---
description: Run a single Redis service on Wodby with the Redis catalog stack and link your application to it. The service listens on port 6379.
---

# Redis

The Wodby Redis catalog stack runs a single Redis service. The current composition and defaults are documented in
[`wodby/stack-redis`](https://github.com/wodby/stack-redis).

## Connect an application

The Redis service listens on port `6379`. It has no HTTP endpoint, so Wodby creates no route for it.

1. Link your application's app service to the Redis app service. See [Links](../../../apps/services.md#links-tab).
2. Read the connection values from the environment variables your app service receives. The linking service chooses
   their names, for example `REDIS_HOST`, `REDIS_PORT` and `REDIS_PASSWORD`, or a single `REDIS_URL`.

A password is always required. Wodby generates it as the `password` token. Open the Redis app service's
**Configuration > Tokens** tab to see it. Do not hardcode the host or copy the password into your repository.

## Choose cache or storage behavior

With the defaults, Redis is a cache. It holds up to 128 MB (`REDIS_MAXMEMORY`). After that it evicts any key, including
keys without an expiry (`REDIS_MAXMEMORY_POLICY` is `allkeys-lru`).

If you store a job queue, sessions or other data that must not disappear, set `REDIS_MAXMEMORY_POLICY` to `noeviction`
and raise `REDIS_MAXMEMORY`. Otherwise Redis drops data silently under memory pressure.

Set these variables on the Redis app service under **Configuration > Variables**. See
[Environment variables](../../../apps/environment-variables.md). They apply on the next deployment. Do not edit the
generated configuration file; it is rewritten on every start.

| Variable | Effect | Default |
| --- | --- | --- |
| `REDIS_MAXMEMORY` | Memory limit | `128m` |
| `REDIS_MAXMEMORY_POLICY` | Eviction policy | `allkeys-lru` |
| `REDIS_DATABASES` | Number of databases | `16` |
| `REDIS_TIMEOUT` | Idle client timeout, in seconds | `300` |
| `REDIS_NOTIFY_KEYSPACE_EVENTS` | Keyspace notifications | empty |

## Data and backups

The stack does not add the optional **Data** volume. Without it nothing is written to disk, and every restart or
deployment starts with an empty Redis. To keep data, add the volume under **Runtime > Volumes** on the Redis app
service and redeploy. Wodby then turns persistence on. Once added, the volume cannot be resized or removed. See
[Volumes](../../../apps/services.md#volumes-tab).

The service has no backup or import support.

## Check that it works

Open a [web terminal](../../../apps/web-terminal.md) on the Redis app service and run:

```bash
redis-cli -a "$REDIS_PASSWORD" ping
```

The answer is `PONG`. Use `config get maxmemory-policy` and `config get appendonly` to see the eviction policy and whether
persistence is on. `info stats` shows `evicted_keys`.
