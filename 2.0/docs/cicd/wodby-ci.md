# Wodby CI

Wodby CI is the built-in CI system for Wodby 2.0. Add the pipeline files to the repository you selected as the build source for a buildable service. Wodby provides `WODBY_BUILD_ID`, which you pass to `wodby ci init` inside the pipeline.

## Pipeline

To use Wodby CI, create `.wodby/pipeline.yml` in the repository that you selected as the build source of a buildable service in your app.

Example:

```yml
version: 0.1

workflows:
  main:
    jobs:
      - build

jobs:
  build:
    steps:
      - clone

      - cache_restore:
          path: ~/.composer
          key: 'composer-{{ hash "composer.lock" }}-v1'

      - run: wget -qO- https://api.wodby.com/v1/get/cli | sh
      - run: wodby ci init $WODBY_BUILD_ID
      - run: wodby ci run -v $HOME/.composer:/home/wodby/.composer -- composer install -n --no-ansi

      - cache_save:
          key: 'composer-{{ hash "composer.lock" }}-v1'
          path: ~/.composer

      - run: wodby ci build
      - run: wodby ci release
      - run: wodby ci deploy
```

You can find more examples in [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0):

- [PHP Wodby CI pipeline](https://github.com/wodby/wodby-ci/blob/2.0/php/wodby/pipeline.yml)
- [Node Wodby CI pipeline](https://github.com/wodby/wodby-ci/blob/2.0/node/wodby/pipeline.yml)

If you need tooling that is not part of your stack, `wodby ci run` can use an explicit image, for example `wodby ci run -i wodby/node:24 -- npm ci`.

### Reference

#### Version

Supported pipeline version is `0.1`.

#### Workflow

A workflow defines which [jobs](#job) run and in what order.

#### Job

A job is a collection of steps. Jobs can run in parallel.

### Step

Step is a single executable command. The official examples use these built-in step types:

- `clone` (to clone your git repository)
- `cache_restore`
- `cache_save`

You can run arbitrary shell commands by using a `run` key:

```yml
jobs:
  build:
    steps:
      - run: echo "run shell command"
```

### Env

You can define environment variables for the entire pipeline at the top level or for a specific job:


```yml
version: 0.1

env:
  FOO: bar

workflows:
  main:
    jobs:
      - build

jobs:
  build:
    env:
      FOO: bar
    steps:
      - clone
```

### Predefined env vars

Wodby CI injects the following environment variables into every job:

- `WODBY_CI` set to `true`
- `WODBY_BUILD_NUMBER` with the Wodby build number
- `WODBY_BUILD_ID` with the Wodby app build ID. This is the value passed to `wodby ci init`
- `WODBY_APP_INSTANCE_ID` with the app instance ID
- `WODBY_APP_NAME` with the app name

In addition to the predefined variables above, Wodby exports app service environment variables and setting-derived variables for the main service container into the build environment.

## Post-deployment scripts

You can additionally create `.wodby/post-deployment.yml` to define post-deployment scripts that should run after all deployments in your app have completed.

The syntax is the same as the [Wodby CI pipeline](#pipeline) except it does not have workflows. All defined jobs run in parallel.

Example:

```yml
version: 0.1

jobs:
  drush-status:
    steps:
      - run: drush status
```

See also the example files in [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0):

- [PHP post-deployment example](https://github.com/wodby/wodby-ci/blob/2.0/php/wodby/post-deployment.yml)
- [Node post-deployment example](https://github.com/wodby/wodby-ci/blob/2.0/node/wodby/post-deployment.yml)

You can skip execution of post-deployment scripts by passing `--skip-post-deploy` to `wodby ci deploy`.
