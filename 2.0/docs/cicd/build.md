# CI build

This page covers the process of the build in CI system, to learn more about builds in general please see [app builds](../apps/builds.md).

The `wodby ci build` will build the specified service or all services if no service is specified. 

The build service essentially runs `docker build` command. Unless a custom `Dockerfile` specified in the service template or via `--dockerfile` flag, the following generic Dockerfile will be used:

```markdown
ARG WODBY_BASE_IMAGE
FROM ${WODBY_BASE_IMAGE}
ARG COPY_FROM
ARG COPY_TO
COPY --chown={{.DefaultUser}}:{{.DefaultUser}} ${COPY_FROM} ${COPY_TO}
```

Here the base image will be used from the current app's stack definition. Values for `COPY_FROM` and `COPY_TO` set to `.` (current directory) by default but can be changed with flags `-from` and `-to`. 

