# CircleCI

## New build

Wodby starts a CircleCI build from the dashboard by rerunning a previously recorded workflow. Link the app service's
Git repository, select a branch or tag, and run the first CircleCI workflow on that ref outside Wodby so the workflow
can be recorded. If the recorded workflow is no longer rerunnable in CircleCI, start it again from CircleCI.

## Build examples with Wodby CLI 2.0

### PHP-based

The following example:

1. Installs dependencies from `composer.json` using the automatic Wodby CLI cache persisted by CircleCI
2. Builds the service images configured for the app
3. Releases image to the registry associated with the app environment
4. Runs deployment of the build for the associated app environment

Make sure you've:

- Added `WODBY_API_KEY` environment variable in CircleCI project settings with [your Wodby API key](../dev/api-keys.md) value
- Added `WODBY_APP_SERVICE_ID` environment variable with the app service ID of the service being built

The public [`wodby/setup-wodby-cli`](https://circleci.com/developer/orbs/orb/wodby/setup-wodby-cli) orb installs the
latest Wodby 2 CLI and initializes the build. Dependency caching remains in the CircleCI configuration so each app can
persist the cache appropriate for its package manager.

```yaml
version: 2.1

orbs:
  wodby: wodby/setup-wodby-cli@1

jobs:
  build:
    machine:
      image: ubuntu-2604:current

    steps:
      - checkout

      - restore_cache:
          keys:
            - composer-v1-{{ checksum "composer.lock" }}
            - composer-v1-

      - wodby/setup:
          app-service-id: $WODBY_APP_SERVICE_ID

      - run:
          name: Install composer dependencies
          command: wodby ci run -- composer install --prefer-dist -n --no-ansi

      ## When you need to use a checkout key for private repositories:
      # - run:
      #     name: Install composer dependencies with private packages
      #     command: wodby ci run \
      #       -v /home/circleci/.ssh/known_hosts:/tmp/.ssh/known_hosts:ro \
      #       -v /home/circleci/.ssh/id_rsa_[your-checkout-key-fingerprint]:/tmp/.ssh/id_rsa:ro \
      #       -s php -- composer install -n

      - save_cache:
          key: composer-v1-{{ checksum "composer.lock" }}
          paths:
            - ~/.composer/cache

      - run: wodby ci build
      - run: wodby ci release
      - run: wodby ci deploy
```

See the [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0) repository for CircleCI examples covering other
application stacks and package managers.
