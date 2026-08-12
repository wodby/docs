# Service build

## Overview

Only services of type `service` can define a build section.

Use build settings when a service can receive a [CI/CD](../cicd/index.md) build image.

The two common patterns are:

1. A service has a build source. Connected sources inherit the app instance's Default CI. Under third-party CI the
   source can be external and identified by app service ID. Public and cloned boilerplate sources use Wodby CI.
2. A service is a build image target, but does not need its own repository connection.

A service with a build source starts the build flow. A build image target without its own build source can still be built by the same pipeline, but it does not have to be built every time. If no build image is attached during deployment, Wodby uses the service's configured image from the manifest or chart.

For an image target, set `build.link` to the name of the service link that resolves to the build-source owner:

```yaml
build:
  link: backend

links:
  - name: backend
    title: Backend
    required: true
    selectors:
      - type: service
```

The named link must be declared by the image-target service. In an app instance, its linked service must have build
configuration with `connect: true` and an actual build source. An image target using `build.link` cannot also enable
`build.connect` or define build boilerplates, because it does not own a separate source.

Mark deployment targets explicitly with `workloads[].containers[].build: true`.

- Services with build configuration must mark at least one container this way.
- Services without build configuration must not define `build: true` on containers.
- More than one container can be marked only when they are expected to receive the same built image.

The target Helm paths are taken from `workloads[].containers[].helm.image` and default to `image.repository`,
`image.tag`, `image.registry`, and `image.pullPolicy`.

### Build boilerplates

Build boilerplates are starter repositories that customers can clone when creating a new project. Each boilerplate
points to a GitHub repository and selects either a branch or a tag. During new app creation, Wodby can import the
selected boilerplate into a new GitHub or GitLab repository. A boilerplate can also reference a custom pipeline file.

One boilerplate can be marked as the default. When no boilerplate is marked as default, Wodby treats the first
boilerplate in the service template as the default.

Boilerplates must include a valid Wodby CI pipeline. Selecting a public boilerplate or cloning one into a new Git
repository overrides the app instance's Default CI for that app service and uses Wodby CI.

### Dockerfile

Services can specify a custom Dockerfile in the service manifest. Use `build.dockerfile` for a path in the same
repository; it is resolved relative to the directory containing `service.yml` and must exist. Use
`build.dockerignore` for the matching ignore file. Wodby CI uses this configuration during
`wodby ci build [service]`.

Use `build.dockerfileContent` or `build.dockerignoreContent` when the content is defined inline in `service.yml`. Do not
specify a path field and its corresponding content field together.

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
