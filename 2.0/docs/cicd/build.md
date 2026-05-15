# CI build

This page covers image builds in CI. To learn more about builds in general see [app builds](../apps/builds.md).

Use `wodby ci build [OPTIONS] [SERVICE]...` to build one or more services from the current app build config. If you do not specify services, the CLI tries to build all buildable services and prioritizes the main service first.

## Dockerfile resolution

For each service, the CLI resolves the Dockerfile in this order:

1. The path passed with `-f, --dockerfile`
2. `<service>_Dockerfile` from the build context
3. The Dockerfile stored in the Wodby app service configuration
4. A generated default Dockerfile

When the CLI generates a Dockerfile it uses:

```dockerfile
ARG WODBY_BASE_IMAGE
FROM ${WODBY_BASE_IMAGE}
ARG COPY_FROM
ARG COPY_TO
COPY --chown={{.DefaultUser}}:{{.DefaultUser}} ${COPY_FROM} ${COPY_TO}
```

`WODBY_BASE_IMAGE` comes from the current stack definition. `COPY_FROM` and `COPY_TO` default to `.` and can be changed with `--from` and `--to`.

The matching ignore file is `<dockerfile>.dockerignore`. If it is not present in the build context, the CLI falls back to the `.dockerignore` from the Wodby service config or to a small default ignore list.

## Build arguments and cache

`wodby ci build` supports additional Docker build args via `--build-arg NAME=VALUE` and can forward environment variables with `--build-arg-env NAME`.

The app build config can also provide build arguments from Wodby service configuration. Only values explicitly marked
as build-scoped are included:

- service settings with `build: true`, using the setting's `var` as the argument name
- service environment variables with `build: true`, using the env var `name`
- app-service environment variables with `build: true`

The CLI passes these values only when the Dockerfile declares a matching `ARG`. Runtime-only settings, runtime-only env
vars, stack env vars, and variable integrations are not passed to builds.

Secret build arguments are not written to the local CI config. The CLI forwards them from environment variables with
matching names. Wodby CI injects these variables automatically; in third-party CI, configure the same names as CI secret
environment variables.

Builds use `docker buildx build --load`, so images remain available locally for `wodby ci release`.

Cache-related flags:

- `--cache-backend auto|local|registry|none`
- `--cache-dir` for local cache
- `--cache-ref` for registry-backed cache
- `--cache-mode` to control cache export mode
- `--cache-from` and `--cache-to` for advanced buildx overrides

With non-DIND builds, `--cache-dir` is enough to enable local cache. In `--dind` mode, `--cache-backend auto` switches to a registry-backed cache reference for each service.

## Examples

```bash
# Build all buildable services
wodby ci build

# Build only the node service
wodby ci build node

# Build nginx from a subdirectory and copy it to a custom path
wodby ci build nginx --from static --to /var/www/html/static
```
