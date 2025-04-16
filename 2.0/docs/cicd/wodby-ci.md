# Wodby CI

Wodby CI is the default CI that provides native integration with Wodby platform such as rerunning CI builds directly from the dashboard. Alternatively, you can use your own CI by creating CI-typed [integration](../integrations/index.md).   

## Pipeline

To use Wodby CI create `.wodby/pipeline.yml` in a git repository that you chose a build source of a buildable service in your app.

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
    - run: wodby ci run -v $HOME/.composer:/home/wodby/.composer -s php -- composer install -n --no-ansi
    - run: wodby ci run -v $HOME/.composer:/home/wodby/.composer -s php -- composer require drush/drush

    - cache_save:
        key: 'composer-{{ hash "composer.lock" }}-v1'
        path: ~/.composer

    - run: wodby ci build php
    - run: wodby ci build nginx --from web --to /var/www/html/web
    - run: wodby ci release
    - run: wodby ci deploy
```

You can find more examples at https://github.com/wodby/wodby-ci

### Reference

#### Version

Currently, there's only one version we support which is `0.1`

#### Workflow

Workflow in Wodby CI is a collection of [jobs](#job) and their run order.

#### Job

A job is a collection of steps. Unlike steps, jobs can be run in parallel.

### Step

Step is a single executable command. There are system commands such as 

- `clone` (to clone your git repository)
- `cache_restore`
- `cache_save`

You can run arbitrary shell commands by using a `run` key:

```
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

## Post-deployment scripts

You can additionally create `.wodby/post-deployment.yml` to define post-deployment scripts that should be run after all deployments in your app completed.

The syntax is the same as [Wodby CI pipeline](#pipeline) except not having workflows, all defined jobs will be run in parallel.

Example:

```yml
version: 0.1

jobs:
  drush-status:
    steps:
    - run: drush status
```
