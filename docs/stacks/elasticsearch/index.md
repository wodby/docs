# Elasticsearch stack documentation

Elasticsearch and Kibana can be configured via environment variables:

* https://github.com/wodby/elasticsearch#environment-variables
* https://github.com/wodby/kibana#environment-variables

## Changelog

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
