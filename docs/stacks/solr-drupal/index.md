# Solr for Drupal stack documentation

The only difference from the generic Solr stack is that core created with a config set from [Search API Solr module](https://www.drupal.org/project/search_api_solr) by default.

!!! info "Default core"
    We automatically create a default solr core named `default` when no cores found.

!!! important "New Solr image"
    Since 1.3.0 Solr image `wodby/solr` has been replaced with `wodby/solr` and `$SOLR_DEFAULT_CONFIG_SET`, see [versions matrix](https://github.com/wodby/solr#drupal-search-api-solr)

See generic [Solr stack](../solr/index.md) documentation to learn how to create and customize cores.

### Drupal 8

Install [Search API Solr module](https://www.drupal.org/project/search_api_solr). Go to `Home » Administration » Configuration » Search and metadata » Search API`, create a new core or edit the default one. In expanded `CONFIGURE SOLR BACKEND` field set specify:

```
HTTP protocol: http
Solr host: solr
Solr port: 8983
Solr path: /solr
Solr core: [NAME OF YOUR CORE]
```

### Drupal 7

Install [Search API Solr module](https://www.drupal.org/project/search_api_solr). Go to `Configuration » Search and metadata » Search API` and select Service class to "Solr service". In expanded settings field set specify:

```
HTTP protocol: http
Solr host: solr
Solr port: 8983
Solr path: /solr/[NAME OF YOUR CORE]
```

!!! warning "Different hostname for stand-alone stacks"
    If you use a stand-alone Solr for Drupal stack for `Solr host` use `Internal hostname` from `[Instance] > Stack > Search Engine` page in case Drupal and Solr stacks deployed on the same server. 

## Changelog

This changelog is for Solr for Drupal stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/solr/releases).

### 2.2.0

- Versions 5.4, 6.4, 7.1-7.4 no longer supported (marked as EOL)
- Versions 7.6, 7.7 added (and 5.5 for Drupal 7)
- Added new search_api_solr config sets (Drupal 8 default config set updated to `8.x-2.7`)    
- Bugfix: attachments indexation did not work in Drupal 7 https://github.com/wodby/solr/issues/5

### 2.1.0

* Added version 7.5
* Add Solr 6/7 variants for Drupal 7 
* search_api_solr version used for config sets now shown in titles and have been updated:
    * Drupal 7: 7.x-1.14 
    * Drupal 8: 8.x-1.2 for Solr 5, 8.x-2.1 for others

### 2.0.1

Solr patch update: 6.6.5

### 2.0.0

* Image `wodby/drupal-solr` now replaced with `wodby/solr` and `$SOLR_DEFAULT_CONFIG_SET`, see [versions matrix](https://github.com/wodby/solr#drupal-search-api-solr) 
* New Solr versions added: 7.4, 7.3 
* Dropped versions 6.3, 6.5, 7.0 
* Config sets and `solr.xml` now symlinked to volume, existing cores won't be affected
* Core directory get deleted when you delete a core via orchestration actions
* Bugfix: duplicated `configsets/configsets` directory

### 1.2.1

* New 7.2 version added
* Patch update: 6.6.3
* Solr 7.x config sources updated to search_api_solr `8.x-2.0-alpha3`

### 1.2.0

* Default [memory request](../config.md#resources) set to 256m

### 1.1.0

* New Solr versions 7.0.1 and 7.1.0 have been added with a config set from search_api_solr `8.x-2.0-alpha2`
* Solr versions updated and freezed: 6.6.2, 6.5.1, 6.4.2, 6.3.0, 5.5.5, 5.4.1
* Config set source search_api_solr updated to `8.x-1.2`
* We now create a default solr core named `default` automatically if no cores found
* Health check timeouts increased to 30 seconds

### 1.0.4

* Solr: fixed persistent data paths configuration

### 1.0.1

* Solr: new versions 6.6 and 6.5 for Drupal 8
* Solr: search_api_solr version updated from to 8.x-1.0 (default solr configs used from this module)
* Solr versions are now frozen https://github.com/wodby/solr#versions

### 1.0.0

Initial release