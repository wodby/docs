# Application Builds

Some [services are buildable](../services/build.md), for such app services we expect a [CI system](../cicd/index.md) to build container images and trigger deployment via Wodby CLI. 

## Build sources and buildable services

1. There are app services that have a connected git repository from a git integration as a build source
2. There are associated app services that also buildable but do not have a build source. We expect users to build images from both of these services during a build and triggering a deployment that provides build information for both of those services

A simple example will be an app with Nginx and PHP services, where a git repository that contains both backend and frontend connected to a PHP service. During the build in addition to backend build (e.g. composer) user can build frontend code (e.g. nodejs) for Nginx. After building container images for the both services a user will run a release (`wodby ci release` to push to associated docker registry) and deployment (`wodby ci deploy`).

## Build info

A build always provides the following information:

- Main app service with the build source (git repository) that provides the build pipeline
- Build number
- Associated stack revision
- CI system that produced this build ([Wodby CI](../cicd/wodby-ci.md) by default)
- Associated git repository
- Related git commit information
- Resulting docker images that should be deployed

## Needs rebuild

Similar to [`needs_redeploy`](deploys.md#needs-redeploy) app instance with buildable services will be marked as `needs rebuild` when buildable services changed. It is to indicate although there were changes they may not have yet applied, for example an environment variable value changed that may affect the build process. 
