# CI build

This page covers image builds in CI. To learn more about builds in general see [app builds](../apps/builds.md).

Use `wodby ci build [OPTIONS] [SERVICE]...` to build one or more services from the current app build config. If you do not specify services, the CLI tries to build all build image targets and prioritizes the main service first.

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

`WODBY_BASE_IMAGE` comes from the current stack definition. `COPY_FROM` and `COPY_TO` default to `.` and can be changed with `--from` and `--to`. When a service sets `build.copySubdir`, that subdirectory is appended to both, so the flags give the roots and the service gives the path within them.

## Building from your own Dockerfile

A Dockerfile taken from the repository, whether by `--dockerfile` or as `<service>_Dockerfile` in the build context, must build from the service image:

```dockerfile
ARG WODBY_BASE_IMAGE
FROM ${WODBY_BASE_IMAGE}
```

In a multi-stage build the final stage must be the one that uses it. After the build the CLI compares image layers to confirm this, and fails when the image is not derived from the service image. Such an image stops receiving service image updates while Wodby continues to report the app service as running the service image version.

Pass `--allow-unmanaged-image` to build anyway. The build then warns, and the image is recorded as unmanaged so the app build view shows that it no longer tracks service image versions.

Two things worth knowing when maintaining your own Dockerfile:

- You do not need to run the service init action. Service images apply it on container start, so a `RUN make init-...` line is redundant, though harmless because the action is idempotent.
- An `ARG` only receives a value when the matching service setting or environment variable is marked as a build argument. An `ARG` with no such value expands to an empty string rather than failing the build, so a `COPY` written in terms of it copies a different path.

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
# Build all build image targets
wodby ci build

# Build only the node service
wodby ci build node

# Build nginx from a subdirectory and copy it to a custom path
wodby ci build nginx --from static --to /var/www/html/static
```
