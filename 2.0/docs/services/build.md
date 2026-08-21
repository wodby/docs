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

Most services do not need one. Wodby CI generates a Dockerfile that builds from the service image and copies the
codebase into it, which is all a typical service requires.

Provide one only when the image needs build steps the generated Dockerfile cannot express, such as compiling
dependencies. Use `build.dockerfile` for a path in the same repository; it is resolved relative to the directory
containing `service.yml` and must exist. Use `build.dockerignore` for the matching ignore file. Use
`build.dockerfileContent` or `build.dockerignoreContent` when the content is defined inline in `service.yml`. Do not
specify a path field and its corresponding content field together.

Preparing the codebase for the image is not a reason to provide one. Service images apply their own init action when
the container starts, so a Dockerfile does not have to run it. To narrow the build to part of the repository, use
`build.copySubdir` below.

### Copying part of the repository

A service that needs only one directory of the repository, such as a web server that serves the docroot while the
application runs in a linked service, sets `build.copySubdir`:

```yaml
build:
  link: backend
  copySubdir: "{{settings.docroot}}"
```

The value is a subdirectory, applied to both the source and the destination, so the path is preserved: the codebase at
`web` in the repository lands at `web` under the image working directory. Both sides use the same value because a web
server and the application it passes requests to must resolve the docroot to the same absolute path.

It may reference a service setting as `{{settings.<name>}}`, so the value follows whatever the user configures rather
than being fixed in the manifest. The setting must be declared by the same manifest and must not be secret; import
fails otherwise, as it does for an absolute path or one containing `..`.

Leave `copySubdir` unset to copy the whole build context, which is the default.

### Build arguments

Docker build arguments are explicit. If a Dockerfile declares an `ARG`, Wodby passes a value only when the
corresponding service setting, service environment variable, or app-service environment variable is marked
`build: true`. This applies to a Dockerfile provided by the service and to one provided by the app being built; the
generated Dockerfile declares only `WODBY_BASE_IMAGE`, `COPY_FROM` and `COPY_TO`.

An `ARG` with no matching build-scoped value is not an error. Docker expands it to an empty string, so a `COPY` written
in terms of it silently copies a different path.

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
