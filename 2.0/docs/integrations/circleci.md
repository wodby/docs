# CircleCI

## Build examples with Wodby CLI 2.0

### PHP-based

The following example:

1. Installs your dependencies from composer.json (using circleci caching)
2. Builds images for php and nginx services (nginx image does not include composer dependencies because we only need static files)
3. Releases image to the registry associated with the app instance
4. Runs deployment of the build for the associated app instance

Make sure you've:
- Added `WODBY_API_TOKEN` environment variable in CircleCI project settings with [your Wodby API Key](../development/api-keys.md) value
- Replaced `WODBY_GIT_REPO_ID` with the git repo ID of the PHP service or added the env var `WODBY_GIT_REPO_ID` with the value

```yaml
version: 2

jobs:
  build:
    machine:
      # Make sure the image is up-to-date.
      image: ubuntu-2204:2023.10.1

    steps:
    - checkout

    - restore_cache:
        keys:
        - composer-v1-{{ checksum "composer.lock" }}
        - composer-v1-

    - run: wget -qO- https://api.wodby.com/v1/get/cli | sh
    - run: wodby ci init $WODBY_GIT_REPO_ID
    - run:
        name: Fix .composer permissions
        command: wodby ci run -v $HOME/.composer:/home/wodby/.composer -s php --user root -- chown -R 1000:1000 /home/wodby/.composer

    - run:
        name: Install composer dependencies
        command: wodby ci run -v $HOME/.composer:/home/wodby/.composer -s php -- composer install -n

    ## When you need to use a checkout key for private repositories:
    #       - run: 
    #           name: Install composer dependencies with private packages
    #           command: wodby ci run \
    #             -v /home/circleci/.ssh/known_hosts:/home/wodby/.ssh/known_hosts \
    #             -v /home/circleci/.ssh/id_rsa_[your-checkout-key-fingerprint]:/home/wodby/.ssh/id_rsa \
    #             -v $HOME/.composer:/home/wodby/.composer \
    #             -s php -- composer install -n

    - save_cache:
        key: composer-v1-{{ checksum "composer.lock" }}
        paths:
        - ~/.composer

    - run: wodby ci build php
    - run: wodby ci build nginx --from web --to /var/www/html/web
    - run: wodby ci release
    - run: wodby ci deploy
```
