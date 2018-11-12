# Elasticsearch stack documentation

You can enable Elasticsearch plugins by listing them via the environment variable `$ES_PLUGINS_INSTALL` separated by comma.

!!! info "Open source version"
    Since version 6.3 we install OSS version of Elasticsearch and Kibana. In older version we disable x-pack plugin by default.

Elasticsearch and Kibana can be configured via environment variables:

* https://github.com/wodby/elasticsearch#environment-variables
* https://github.com/wodby/kibana#environment-variables

## Changelog

This changelog is for Elasticsearch stack on Wodby, to see images changes see tags description on repository page: [elasticsearch](https://github.com/wodby/elasticsearch/releases) and [kibana](https://github.com/wodby/kibana/releases).   

### 2.1.2

Elasticsearch and Kibana patch updates: 5.6.13

### 2.1.1

Elasticsearch and Kibana patch updates: 5.6.12

### 2.1.0

* Rebased to Alpine Linux 3.8 with OpenJDK 8.171.11 (JRE)
* Added new versions 6.3 for ES and Kibana
* For version 6.3+ we now install OSS version of ES and Kibana (without x-pack)
* Kibana and ES patch updates: 5.6.11

### 2.0.1

* Default [memory request](../config.md#resources) set to 512m

### 2.0.0

* Elasticsearch and Kibana images rebuilt to Alpine Linux
* Elasticsearch and Kibana 5 updated to 5.6.6
* New line `6` (6.1) for Elasticsearch and Kibana, now default
* Updated the list of environment variables for configuration, see http://github.com/wodby/elasticsearch and http://github.com/wodby/kibana

### 1.0.1

Make elasticsearch accessible from the outside.

### 1.0.0

Initial release
