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

You can set up CI/CD workflow for your application by integrating Wodby with third-party CI tools. Build can be performed on any CI tools with Wodby CLI. 

Big picture:

1. Deploy an app based on a managed stack that supports CI deployments or custom stack with at least one service having [`deployment.type=ci`](../stacks/template.md#deployment)
2. [Get](#wodby-cli) Wodby CLI tool or its docker image
3. [Initialize](#init) the build by providing an API key scoped to the app's organization and the UUID of your app instance
4. [Build](#build) images with your codebase. Images will be based on the images from your stack
5. Push ([release](#release)) images to a private docker registry we provide you (or any other registry)
6. [Deploy](#deploy) the build (a set of images) to your app instance

!!! caution "Do not store your Wodby API key in git repository"
    Do not share your Wodby API key or store it in a git repository. Create a key scoped to the application's organization and add it as a secret environment variable in your CI settings. The dashboard shows the secret only once.

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

This command will gather build information about your instance such as services (images) that can be built and private docker registry credentials. All builds must start with the init. To perform this step you must have a [Wodby API key](../dev.md#api-keys) scoped to the instance's organization, exported as `$WODBY_API_KEY` or provided via `--api-key`. Make sure the key is stored securely and is not publicly exposed.

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

By default, commands using the bind-mounted build context run with the CI workspace's numeric user and group. This
keeps files created by Composer, npm, and other tools owned by the checkout user without changing ownership of the
existing codebase. When the CLI applies this numeric identity, it uses `HOME=/tmp` unless you pass `HOME` explicitly.

For a managed stack in a recognized native CI provider, `wodby ci init` recursively prepares the bind-mounted checkout
for the default service image user before running the stack initializer. Custom stacks and unrecognized environments
leave bind-mounted ownership unchanged unless you pass `--fix-permissions`. The managed initializer keeps the image's
default user and entrypoint so image-provided actions such as `init-drupal` remain available. An explicit
`wodby ci run --user` overrides the workspace identity used by subsequent commands.

In docker-in-docker mode, the checkout is stored in a Docker-managed data volume. During initialization, the CLI
resolves the default service image user to a numeric user and group and prepares that volume with its utility image.
The application image therefore does not need to provide `chown` or a shell for ownership preparation. The managed
initializer and subsequent `wodby ci run` commands keep the selected image's default user and entrypoint.

##### Dependency caches

`wodby ci run` automatically configures dependency caches for supported images:

| Profile | Package manager variable | Path inside the container | Native host path |
| --- | --- | --- | --- |
| `npm` | `NPM_CONFIG_CACHE` | `/tmp/wodby-cache/npm` | `~/.npm` |
| `composer` | `COMPOSER_CACHE_DIR` | `/tmp/wodby-cache/composer` | `~/.composer/cache` |
| `bundler` | `BUNDLE_USER_CACHE` | `/tmp/wodby-cache/bundler` | `~/.bundle/cache` |
| `uv` | `UV_CACHE_DIR` | `/tmp/wodby-cache/uv` | `~/.cache/uv` |

When the CLI runs natively against the host Docker daemon, it mounts each cache from the package manager's
conventional path under the current user's home directory. Configure the CI provider to persist the applicable path
between jobs. For example, a Composer job can cache:

```yml
cache:
  directories:
    - ~/.composer/cache

script:
  - wodby ci run -s php -- composer install -n
```

For docker-in-docker builds, `wodby ci init` creates an internal cache volume at `/tmp/wodby-cache`. It imports
project-local `.wodby-ci-cache/<profile>` staging directories during initialization and exports updated profiles after
each cache-enabled `wodby ci run`. Configure the CI provider to persist the applicable staging directory and add
`.wodby-ci-cache/` to `.gitignore`. Commands keep the image's default user and entrypoint in this mode, and only the
internal data volumes are prepared for writing. No host cache-directory mount is required.

Cache persistence is optional. Missing staging directories require no setup, and failures while importing, preparing,
or exporting automatically detected caches produce a warning instead of failing initialization or the command. A
profile explicitly requested with `--cache PROFILE` remains strict during command setup and export.

Use `--cache npm`, `--cache composer`, `--cache bundler`, or `--cache uv` to force a profile for another image. Use
`--no-cache` to disable automatic caching. Setting `WODBY_CI_CACHE_DIR` explicitly replaces the default native home
paths or docker-in-docker staging root with a `ROOT/<profile>` layout. Explicit package-manager cache environment
variables and volumes targeting the container paths above take precedence. Specifying `--user` disables automatic
profile detection; combine it with `--cache PROFILE` when both overrides are needed.

If you need to access private repositories you should add a checkout ssh key to your environment (please refer to your CI provider documentation), then mount the key and `.known_hosts` file (to avoid interactive dialogues), example for CircleCI:

```yml
- run: 
    name: Install composer dependencies with private packages
    command: wodby ci run \
        -v /home/circleci/.ssh/known_hosts:/tmp/.ssh/known_hosts:ro \
        -v /home/circleci/.ssh/id_rsa_[your-checkout-key-fingerprint]:/tmp/.ssh/id_rsa:ro \
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
