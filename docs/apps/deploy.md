# Code deployment 

## Direct git deployments

!!! info "Only for Drupal and WP"
    This deployment option available only for [Drupal](../stacks/drupal/index.md) and [WordPress](../stacks/wordpress/index.md) stacks and their forks

You can connect your git repository to Wodby and use it as a codebase source for your applications. On code deployment we will perform pull from the target branch and run [post-deployment scripts](post-deployment-scripts.md) (if enabled). 

Additionally, you can run deployment automatically every time you push code to a git branch (all instances using this branch will be deployed):

1. Configure git hooks for your git repository 
2. Navigate to `Instance > Deployment > Settings` and check `Automatic deploy` option

For details instructions how to connect a repository and configure hooks see the following articles:

* [GitHub](../integrations/github.md) 
* [BitBucket](../integrations/bitbucket.md) 
* [GitLab](../integrations/gitlab.md) 
* [Custom git provider](../integrations/custom.md) 

## CI/CD

Sometimes direct git integration may not be enough for a few reasons:

* Build stage is a must have for repositories with dependencies (e.g. npm, composer)
* You need to run tests
* Direct git deployment cannot be used for custom stacks and cluster deployments
* With CI/CD you have build artifacts like docker images that you can download locally
* With CI/CD you can rollback build (feature TBA)

### Wodby CI

!!! tip "Coming soon"
    We plan to replace direct git integration with our built-in CI system

### Via third-party CI

!!! question "Docker in docker or VM?"
    If your CI tool can run builds both in Docker and Virtual Machine (as CircleCI does) we recommend using the latter. Despite Wodby CLI can work inside docker (and we have the [image](https://hub.docker.com/r/wodby/wodby-cli/) you can use), it will work slower because building docker images inside docker is less efficient 

You can set up CI/CD workflow for your application by integrating Wodby with third-party CI tools. Build can be performed on any CI tools with [Wodby CLI](https://github.com/wodby/wodby-cli). The build usually consist of the following stages: init, build, deploy and release:

Big picture:

* You deploy your app instance based on a managed stack or custom stack with at least one service having [`deployment.type=ci`](../stacks/template.md#deployment)
* You build images with your codebase. Images based on the images in your stack ([build](#build))
* You push images to a private docker registry we provide you (or your own registry) ([release](#release)) 
* You deploy images to your application instance ([deploy](#deploy))

#### `init`

```shell
wodby ci init [INSTANCE UUID]
```

This command will gather build information about your instance such as services (images) that can be built and private docker registry credentials. All builds must start with the init. To perform this step you must have your [Wodby API key](../account.md#api-key) exported as `$WODBY_API_KEY` or provided via `--api-key`. Make sure the key is secured and not exposed to public. 

#### `build`

During the build stage you can prepare your codebase for the build by running `wodby ci run` which is basically a wrapper of `docker run` that already has a mounted codebase. You can either specify a docker image that runs a command:

```shell
wodby ci run -i wodby/node:8 -- yarn install
wodby ci run -i wodby/node:9 -p path/to/frontend -- yarn install
```

or specify a service name from stack:

```shell
wodby ci run -s backend -- composer install --prefer-dist -n -o --no-dev
```

you can use bind mounts to utilize caching capabilities of your CI tool (`.travis.yml` example):

```yml
cache:
  directories:
    - /home/travis/.composer/cache

script:
  - wodby ci run -v $HOME/.composer:$HOME/.composer -s php -- composer install
```

Once the codebase is ready you can run the build:

```shell
# Build all ci services
wodby ci build 
# Build php service
wodby ci build php
# Build all services starting with node-
wodby ci build node-*
# Build php service with the content from the current directory 
wodby ci build php --from ./
wodby ci build node --from ./ --to /usr/src/app
```

Or you can build from your own `Dockerfile`:

```shell
wodby ci build --dockerfile /path/to/my/Dockerfile
```

If you're using custom `Dockerfile` make sure it starts with the following lines to make sure it will be based on the image from your stack: 

```
ARG WODBY_BASE_IMAGE
FROM ${WODBY_BASE_IMAGE}
```

By default we build images with the name (tag) of a private docker registry we provide. But you can use your own registry:

```shell
wodby ci build -t my-private-docker-hub/repository
``` 

!!! tip "Docker registry"
    Wodby does provide a private docker registry `registry.wodby.com` used by default that you can access with your Wodby user email/password. You can use custom docker registry during the build but if it's a private one make sure to add the appropriate [docker registry integration](../integrations/docker-registry.md) so servers where you deploy instances can access your images.

#### `release`

Once images are built, you can push them to a docker registry:

```shell
# Push all images to the default docker registry 
wodby ci release
# Push to a custom docker registry
wodby ci release -t my-private-docker-hub/repository
# Additionally push with the tag of the current git branch name 
wodby ci release -t my-private-docker-hub/repository -b
``` 

#### `deploy`

```shell
# Deploy all services from the default docker registry
wodby ci release
# Deploy all services from a custom docker registry
wodby ci release -t my-private-docker-hub/repository
```

#### Examples

You can find build examples for different CI services such as CircleCI, TravisCI, BitBucket pipelines and custom shell scripts at https://github.com/wodby/wodby-ci 
