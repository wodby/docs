# Solr stack documentation

Solr can be configured via environment variables available listed at https://github.com/wodby/solr

## Authentication

- Solr (except when run in Solr Cloud mode) does not have authentication by default but you can add [basic auth](../../apps/domains.md#basic-auth) for the solr admin UI domain
- ⚠️ Solr in Solr Cloud already provides authentication which conflicts with the domains basic auth, you should **not** enable basic auth for Solr domain if you're running the Solr Cloud mode. The default auth username is `solr` and the default randomly generated password can be found on the "App instance > Stack > Solr" page, you can override it by adding a custom `$SOLR_CLOUD_PASSWORD` environment variable to the Solr service

## Creating solr collections

You can create new cores via Solr admin UI

## Creating solr core

You can create new cores via Solr admin UI or create it manually from CLI with additional parameters:

### Wodby environment

* Go to `Instance > Stack > Search Engine` page
* Copy and execute `Access container` on your host server to access the container with Solr
* Copy `Create Solr core` command (edit to change core name), execute it inside of the container

### Local environment

1. Access a running Solr container via `make shell solr` or `docker compose exec solr sh`
2. Create a core
```shell
make create core=[core name] -f /usr/local/bin/actions.mk
```

## Reloading solr core

You can reload the core from the Solr admin dashboard or by executing the following orchestration action from the container with running Solr:
```shell
make reload core=[core name] -f /usr/local/bin/actions.mk
```  

## Customizing solr core

By default, we create cores with a reference to a config set, this means that a core does not have its own config but instead uses config files of pre-existing configuration. Available config sets listed under `configsets/*` in the default working directory. To learn which config set used in your core navigate to your core directory, it's a directory in the default working dir (`/opt/solr/server/solr`) that matches your core name. In this directory you'll find `core.properties` file that contains `configSet=` line where a currently used config set specified.

Now there two ways how you can customize your core config:

### 1. By creating new config set

Use this approach when you'll need to use your customized config for multiple cores. 

1. Access the container with running Solr
2. Use existing config set as your boilerplate by copying a directory under `configsets/*`
3. The name of directory under `configsets/*` will be the name of your config set
4. Once the config set is ready update `configSet=` line in `core.properties` file inside your core directory
5. [Reload core](#reloading-solr-core)

!!! warning "Do not modify predefined config set"
    Do not modify config sets that come with the image because all changes will be lost after a container restart.

### 2. By moving configuration to core

Use this approach when you'll need a unique configuration per core. 

1. Access the container with running Solr
2. Use existing config set as your boilerplate by copying `configsets/[CONFIG SET]/conf` to `[CORE NAME]/conf`
3. Once the config set is ready delete `configSet=` line in `core.properties` file inside your core directory
4. [Reload core](#reloading-solr-core)

## Changelog

This changelog is for Solr stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/solr/releases)

### 2.7.4

⬆️ Solr 9.10.1

### 2.7.3

⬆️ Solr 9.10.0

### 2.7.2

- ⬆️ Solr 9.9.0
- 📜 Introduced `$SOLR_STANDALONE` to run Solr in standalone mode

### 2.7.1

⬆️ Solr 9.8.1

### 2.7.0

- ⭐️ Added Solr 9
- 🪦 Solr 8 has reach end of life

### 2.6.3

🐞 Bugfix: zookeeper data was not persistent

### 2.6.2

- 🐞 Solr bugfix: default collection creation in init action failed in Solr cloud mode during https://github.com/wodby/solr/issues/20
- 🏔 Alpine Linux upgraded to 3.17.3, 3.16.5

### 2.6.1

⬆️ Solr 8.11.2

### 2.6.0

- 🚨 Solr in Solr Cloud mode now generates a random password, you should update it. You can find password on "Instance > Stack > Solr" page, read more in [authentication](#authentication) section.
- 🔒 Solr running in Solr Cloud mode now forbids unauthorized access to all pages in admin UI

### 2.5.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- 🪦 Solr 7.5, 7.6 will no longer get updates (update to 7.7)
- 🏔 Alpine Linux updated to 3.15

### 2.4.0

- ⭐️ Added Zookeeper service
- ⭐️ Added Solr Cloud support for Solr

### 2.3.20

⬆️ Solr 8.11.1

### 2.3.19

- 🚨 Fix for [CVE-2021-44228 ](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q)
- 🥶 Base image ([wodby/base-solr](https://github.com/wodby/base-solr)) rebased to [wodby/openjdk](https://github.com/wodby/openjdk) with frozen Alpine 3.13

### 2.3.18

⬆️ Solr 8.11.0

### 2.3.17

⬆️ Solr 8.10.1

### 2.3.16

⬆️&nbsp; Solr 8.10.0

### 2.3.15

⬆️&nbsp; Base image Alpine Linux updated to 3.13.5

### 2.3.14

⬆️&nbsp; Solr 8.8.2

### 2.3.13

⬆️&nbsp; Solr 8.8.1

### 2.3.12

⬆️&nbsp; Solr 8.8.0

### 2.3.11

- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 2.3.10

Solr 8.7.0

### 2.3.9

Solr 8.6.2

### 2.3.8

Solr 8.6.0

### 2.3.7

Solr 8.5.2

### 2.3.6

Solr 8.5.1, 7.7.3

### 2.3.5

Solr 8.5.0 

### 2.3.4

Solr 8.3.1

### 2.3.3

Solr 8.3.0

### 2.3.2

Alpine Linux updated to 3.10.2 for Solr images

### 2.3.1

- Solr updated to 8.2.0
- We now run upgrade action that removes `default` core if it has a broken config set (so it can be automatically recreated). NOT applicable to EOL versions (6.4, 7.1, 7.2, 7.3, 7.4)

### 2.3.0

- Solr updated to 7.7.2
- Added new Solr 8.1 
- Bugfix: `$SOLR_HEAP` did not have any effect
- Images rebased to wodby/base-solr (see README at https://github.com/wodby/base-solr)

### 2.2.2

- Solr updated to 6.6.6
- Alpine Linux updated to 3.9.4

### 2.2.1

Alpine Linux updated to 3.9.3

### 2.2.0

- Versions 5.4, 6.4, 7.1-7.4 no longer supported (marked as EOL)
- Versions 7.6, 7.7 added     

### 2.1.0

* Added version 7.5

### 2.0.1

Solr patch update: 6.6.5

### 2.0.0

* New Solr versions added: 7.4, 7.3 
* Dropped versions 6.3, 6.5, 7.0 
* Config sets and `solr.xml` now symlinked to volume, existing cores won't be affected
* Core directory get deleted when you delete a core via orchestration actions
* Bugfix: duplicated `configsets/configsets` directory

### 1.2.1

* New 7.2 version added
* Patch update: 6.6.3

### 1.2.0

* Default [memory request](../config.md#resources) set to 256m

### 1.1.0

* New Solr versions 7.0.1 and 7.1.0 have been added
* Solr versions updated and freezed: 6.6.2, 6.5.1, 6.4.2, 6.3.0, 5.5.5, 5.4.1
* We now create a default solr core named `default` automatically if no cores found
* Health check timeouts increased to 30 seconds

### 1.0.3

* Solr: fixed persistent data paths configuration

### 1.0.1

* New 6.6 and 6.5 versions
* Solr versions are now frozen https://github.com/wodby/solr#versions

### 1.0.0

Initial release
