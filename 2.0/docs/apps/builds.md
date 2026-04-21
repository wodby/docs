# Application Builds

Some app services are [buildable](../services/build.md). For those services, a [CI system](../cicd/index.md) builds container images and then triggers deployment through the Wodby CLI.

## Build sources and buildable services

The two common patterns are:

1. An app service has a connected Git repository and acts as the main build source.
2. Other app services are also buildable, but do not have their own separate build source. They still produce images as part of the same build and deployment flow.

For example, an app may have `php` and `nginx` services while a single Git repository contains both backend and frontend code. The repository may be connected to the PHP service as the main build source, but the build still produces images for both services. After the images are built, you release them with `wodby ci release` and deploy them with `wodby ci deploy`.

## Build info

A build records:

- the main app service that owns the build source
- the build number
- the associated stack revision
- the CI system that produced the build, such as [Wodby CI](../cicd/wodby-ci.md)
- the related Git repository and commit information
- the resulting container images intended for deployment

## Needs rebuild

Like [`needs redeploy`](deploys.md#needs-redeploy), `needs rebuild` is a status that tells you build-related changes exist but have not yet been applied through a new build.

A typical example is an environment-variable change that affects the build process.
