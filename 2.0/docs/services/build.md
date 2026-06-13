# Service build

## Overview

Only services of type `service` can define a build section.

Use build settings when a service can receive a [CI/CD](../cicd/index.md) build image.

The two common patterns are:

1. A service has a connected Git repository as its build source.
2. A service is a build image target, but does not need its own repository connection.

A service with a build source starts the build flow. A build image target without its own build source can still be built by the same pipeline, but it does not have to be built every time. If no build image is attached during deployment, Wodby uses the service's configured image from the manifest or chart.

Mark deployment targets explicitly with `workloads[].containers[].build: true`.

- Services with build configuration must mark at least one container this way.
- Services without build configuration must not define `build: true` on containers.
- More than one container can be marked only when they are expected to receive the same built image.

The target Helm paths are taken from `workloads[].containers[].helm.image` and default to `image.repository`,
`image.tag`, `image.registry`, and `image.pullPolicy`.

### Build templates

Build templates are starter repositories that customers can clone when creating a new project. Each template points to
a GitHub repository and selects either a branch or a tag. During new app creation, Wodby can import the selected template
into a new GitHub or GitLab repository. A template can also reference a custom pipeline file.

One template can be marked as the default. When no template is marked as default, Wodby treats the first template in the
service template as the default.

### Dockerfile

Services can also specify a custom Dockerfile path in the same repository. Wodby CI uses it during `wodby ci build [service]`.

### Build arguments

Docker build arguments are explicit. If a service Dockerfile declares an `ARG`, Wodby passes a value only when the
corresponding service setting, service environment variable, or app-service environment variable is marked
`build: true`.

Runtime values are not passed to image builds by default. This keeps deployment-only configuration and integration
credentials out of the build environment unless a value is deliberately marked as a build input.

For service templates:

- set `build: true` on an `env` item when its `name` matches a Dockerfile `ARG`
- set `build: true` on a `settings` item when its `var` matches a Dockerfile `ARG`
- set `runtime: false` together with `build: true` for values that are needed only during image build

App-service environment variables can also be marked as runtime, build, or both from the app service configuration.
Build-scoped app-service env vars are allowed only on app services with build configuration.

Variable integrations and stack environment variables are runtime-only and are not passed as build arguments.

## Template

Build information is defined under the [`build` section](template.md#build) in a service template.

Container build targets are part of [service workloads](workloads.md).
