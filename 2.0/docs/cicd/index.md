# CI/CD

Wodby provides the built-in [Wodby CI](wodby-ci.md) to build, release and deploy your images stacks. Alternatively, you can use your own CI/CD system to build and push images to Wodby registry, for more see [CI integrations](../integrations/types.md#cicd). Both approaches utilize [Wodby CLI](../dev/cli.md) to continuously build and deploy your applications in four steps:

## 1. Init

Wodby CLI fetches information about your application stack during
`wodby ci init` step: Dockerfiles for services, their image, associated [docker registry](docker-registry.md).

## 2. [Build](build.md)

Step `wodby ci build [service]` runs
`docker build` for all (or specific) [buildable services](../services/build.md). You can optionally specify a custom Dockerfile or change the build context.

## 3. Release

Step
`wodby ci release` pushes built docker images to the associated registry. By default, we provide [Wodby Registry](wodby-registry.md), but you can also use your own registry such as Docker Hub, for more see [Docker registry integrations](../integrations/types.md#docker-registry).

## 4. [Deploy](deploy.md)

Step
`wodby ci deploy` Sends information about the build (services and their built images) to Wodby API. Wodby will then run a deployment of the built services with provided options (e.g. force deploy all services, skip post-deployment scripts).  

