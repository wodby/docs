# Application Builds

Some app services have [build configuration](../services/build.md). For those services, a [CI system](../cicd/index.md) can build container images and then trigger deployment through the Wodby CLI.

## Build sources and image targets

The two common patterns are:

1. An app service has a connected Git repository and acts as the main build source.
2. Other app services are build image targets but do not have their own separate build source. They can produce images as part of the same build and deployment flow.

For example, an app may have `php` and `nginx` services while a single Git repository contains both backend and frontend code. The repository may be connected to the PHP service as the main build source, but the build still produces images for both services. After the images are built, you release them with `wodby ci release` and deploy them with `wodby ci deploy`.

Build image targets without their own build source are optional. If a build does not produce an image for one of those services, Wodby deploys the service with the configured image from the service manifest or chart. This lets pipelines build `nginx` only when the app needs custom static assets, while still allowing `nginx` to deploy normally as part of the stack.

## Build info

A build records:

- the main app service that owns the build source
- the build number
- the associated stack revision
- the CI system that produced the build, such as [Wodby CI](../cicd/wodby-ci.md)
- the related Git repository and commit information
- the resulting container images intended for deployment

## Void build images

You can void build images when you want to remove old image outputs from future deployment use without deleting the
build record itself. Voided images remain visible in build history, but Wodby blocks deployments that reference them.

Open the build details page and use **Void build images**. The action is available only when all of these conditions are
met:

- the build is not pending or active
- the build has at least one image-bearing app service build that has not already been voided
- none of the build's app service images is currently used by an app service or the current deployment

Voiding a build marks all eligible image-bearing app service builds from that build as voided. A build can show one of
these image statuses:

- `None`: no build images are voided, or the build has no recorded service-build images
- `Partially voided`: some image-bearing app service builds are voided
- `Voided`: all image-bearing app service builds are voided

If a build image is currently deployed, create and deploy a newer build first. After the older image is no longer used,
you can void it.

## Needs rebuild

Like [`needs redeploy`](deploys.md#needs-redeploy), `needs rebuild` is a status that tells you build-related changes exist but have not yet been applied through a new build.

A typical example is changing a build-scoped setting or app-service environment variable. Runtime-only environment
variable and setting changes mark the app service for redeploy instead.
