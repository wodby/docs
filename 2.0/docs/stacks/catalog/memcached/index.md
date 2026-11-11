---
description: Run a single Memcached service on Wodby with the Memcached catalog stack and link your application to it. The service listens on TCP port 11211.
---

# Memcached

The Wodby Memcached catalog stack runs a single Memcached service. The current composition and defaults are documented
in [`wodby/stack-memcached`](https://github.com/wodby/stack-memcached).

## Connect an application

The service listens on TCP port `11211`. UDP is switched off. It has no HTTP endpoint, so Wodby creates no route for it.

Link your application's app service to the Memcached app service. See [Links](../../../apps/services.md#links-tab). The
app service receives the host and port in variables named by the linking service. Read them in code instead of
hardcoding the host.

Memcached has no password, and Wodby generates no token for it. Access is limited to the environment's internal network.

## Settings

Change these under **Configuration > Settings** on the Memcached app service. Do not use a command or a configuration
file.

| Setting | Variable | Default |
| --- | --- | --- |
| **Cache memory (MB)** | `MEMCACHED_MEMORY` | `64` |
| **Worker threads** | `MEMCACHED_THREADS` | `4` |
| **Maximum connections** | `MEMCACHED_MAX_CONNECTIONS` | `1024` |

**Cache memory (MB)** covers cached items only. The process uses more, so set the container memory limit higher under
**Runtime > Resources**.

## Data loss

Memcached stores nothing on disk, and the service has no volume. Every restart and every deployment empties the cache,
because the service is replaced rather than updated in place. When the item memory is full, Memcached evicts the least
recently used items. Do not keep data here that you cannot rebuild.

## Check that it works

Open a [web terminal](../../../apps/web-terminal.md) on the Memcached app service and run:

```bash
make check-ready -f /usr/local/bin/actions.mk
printf 'stats\r\nquit\r\n' | nc localhost 11211
```

The first command reports whether the server answers. The second shows `limit_maxbytes`, `curr_items` and `evictions`.
