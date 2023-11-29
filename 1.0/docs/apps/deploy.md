# Code deployment 

## Direct git deployments

!!! info "Only for Drupal and WP"
    Direct git deployment is available only for [Drupal](../stacks/drupal/index.md) and [WordPress](../stacks/wordpress/index.md) stacks and their forks

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

* Build stage is a must-have for repositories with dependencies (e.g. npm, composer)
* You need to run tests
* Direct git deployment cannot be used for custom stacks and cluster deployments
* With CI/CD you have build artifacts like docker images that you can download locally

### Via third-party CI

!!! warning "Not fully supported by forked stacks"
    Since the CI deployment was added later only certain version of managed stacks support it and that's
    why it's not officially supported by forked stacks (we cannot tell if images are compatible).
    This deployment method however supported by custom stacks (that do not have `metadata.type` specified in the stack manifest).
    You technically still can run CI deployments via API but the _"App > Deployment"_ tab won't reflect any of that in addition to other limitations.

You can set up CI/CD workflow for your application by integrating Wodby with third-party CI tools. Build can be performed on any CI tools with Wodby CLI. 

Big picture:

1. Deploy an app based on a managed stack that supports CI deployments or custom stack with at least one service having [`deployment.type=ci`](../stacks/template.md#deployment)
2. [Get](#wodby-cli) Wodby CLI tool or its docker image
3. [Initialize](#init) the build by providing your Wodby API key and UUID of your app instance
4. [Build](#build) images with your codebase. Images will be based on the images from your stack
5. Push ([release](#release)) images to a private docker registry we provide you (or any other registry)
6. [Deploy](#deploy) the build (a set of images) to your app instance

!!! caution "Do not store your Wodby API key in git repository"
    Do not share your personal Wodby API key. Do not store it in git repository, instead add it as a secret environment variable in your CI settings.

#### Wodby CLI

!!! tldr "VM-based builds over docker-in-docker"
    If your CI tool can run builds both in Docker and Virtual Machine (docker daemon must be available) we recommend using the latter because it's faster

You can install the latest stable Wodby CLI (Linux amd64) tool during the build like this:

```shell
wget -qO- https://api.wodby.com/api/v1/get/cli | sh
```

If you want to install it locally for other systems such as macOS or Windows, or install a specific version follow the instructions at https://github.com/wodby/wodby-cli

Or you can use [`wodby/wodby-cli`](https://hub.docker.com/r/wodby/wodby-cli/) docker image if your CI supports only docker-based builds

#### Init

```shell
wodby ci init [INSTANCE UUID]
```

This command will gather build information about your instance such as services (images) that can be built and private docker registry credentials. All builds must start with the init. To perform this step you must have your [Wodby API key](../dev.md#api-keys) exported as `$WODBY_API_KEY` or provided via `--api-key`. Make sure the key is secured and not exposed to public. 

#### Build

!!! tldr "Services available during the build"
    If you're building a managed stack, the list of services eligible for the build is hardcoded and you can find it in [a stack documentation](../stacks/index.md). If you're building a custom stack, all services that have [`deployment.type=ci`](../stacks/template.md#deployment) will be available
    
During the build stage you can prepare your codebase for the build by running `wodby ci run` which is basically a wrapper of `docker run`. 

You can either specify a docker image that runs a command:

```shell
wodby ci run -i wodby/node -- yarn install
wodby ci run -i wodby/node -p path/to/frontend -- yarn install
```

Or specify a service name from your stack, the image of your current stack version will be used:

```shell
wodby ci run -s backend -- composer install -n
```

You can use bind mounts on libraries cache directories to utilize caching capabilities of your CI tool (`.travis.yml` example):

```yml
cache:
  directories:
    - /home/travis/.composer

script:
  - wodby ci run -v $HOME/.composer:/home/wodby/.composer -s php -- composer install -n
```

In some environments like CircleCI (where uid is different from `1000`) you also need to fix your cache directory permissions before mounting them in `wodby ci run` command:

```shell
- run: wodby ci run -v $HOME/.composer:/home/wodby/.composer --user root -- chown -R 1000:1000 /home/wodby/.composer
```

If you need to access private repositories you should add a checkout ssh key to your environment (please refer to your CI provider documentation), then mount the key and `.known_hosts` file (to avoid interactive dialogues), example for CircleCI:

```yml
- run: 
    name: Install composer dependencies with private packages
    command: wodby ci run \
        -v /home/circleci/.ssh/known_hosts:/home/wodby/.ssh/known_hosts \
        -v /home/circleci/.ssh/id_rsa_[your-checkout-key-fingerprint]:/home/wodby/.ssh/id_rsa \
        -v $HOME/.composer/cache:/home/wodby/.composer/cache \
        -s php -- composer install -n
```

Once the codebase is ready you can run the build via `wodby ci build` which is a wrapper of `docker build`. By default the build command builds a new image based on the image of a service you specified, and copies codebase (contents of the current directory, same as `--from \.`) to service's image default working directory:

```shell
# Build all ci services' images
wodby ci build 
# Same thing
wodby ci build --from \.
# Build php service image 
wodby ci build php
# Build all images of services starting with node-
wodby ci build node-*
# Build php service image with the contents from ./build directory
wodby ci build php --from ./build
# Build node service image with the contents from ./build directory to /usr/src/app directory inside node image 
wodby ci build node --from ./build --to /usr/src/app
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

#### Release

!!! tldr "Docker registry"
    Wodby provides a private docker registry `registry.wodby.com` which used by default. You can use custom docker registry during the build but if it's a private one make sure to add the appropriate [docker registry integration](../integrations/docker-registry.md) so servers where you deploy instances can access your images.

!!! question "How to download images?"
    Once you deployed your first build you can find images' URLs on `Instance > Stack` page. You can get those images locally by running `docker login registry.wodby.com` and entering your Wodby user's email/password.  

Once images are built, you can push them to a docker registry:

```shell
# Push all images to the default docker registry 
wodby ci release
# Push images of specific services 
wodby ci release php node
# Push to a custom docker registry
wodby ci release -t my-private-docker-hub/repository
# Additionally push with the tag of the current git branch name 
wodby ci release -t my-private-docker-hub/repository -b
``` 

#### Deploy

```shell
# Deploy all services from the default docker registry
wodby ci deploy
# Deploy specific services
wodby ci deploy php crond
# Deploy all services from a custom docker registry
wodby ci deploy -t my-private-docker-hub/repository
```

#### Examples

You can find build examples for different CI services such as CircleCI, TravisCI, BitBucket pipelines and custom shell scripts at https://github.com/wodby/wodby-ci 
