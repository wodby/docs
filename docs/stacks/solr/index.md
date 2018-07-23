# Solr stack documentation

!!! info "Default core" 
    Since 1.1.0 we automatically create a default solr core named `default` when no cores found.

All environment variables available for Solr configuration can be found at https://github.com/wodby/solr

## Creating solr core

You can create new cores via Solr admin UI or create it manually from CLI with additional parameters:

* Go to `Instance > Stack > Search Engine` page
* Copy and execute `Access container` on your host server to access the container with Solr
* Copy `Create Solr core` command (edit to change core name), execute it inside of the container. Response `200` means that the core has been successfully created.

## Changelog

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
