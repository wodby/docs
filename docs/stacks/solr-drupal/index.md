# Solr for Drupal stack documentation

The only difference from [Solr stack](../solr/index.md) is that core created with a config set from [Search API Solr module](https://www.drupal.org/project/search_api_solr) by default, for more details on the version see https://github.com/wodby/drupal-solr.

!!! info "Default core"
    We automatically create a default solr core named `default` when no cores found.

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