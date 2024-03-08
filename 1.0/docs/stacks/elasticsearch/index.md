# Elasticsearch stack documentation

You can enable Elasticsearch plugins by listing them via the environment variable `$ES_PLUGINS_INSTALL` separated by comma.

!!! info "Open source version"
    Since version 6.3 we install OSS version of Elasticsearch and Kibana. In older version we disable x-pack plugin by default.

Elasticsearch and Kibana can be configured via environment variables:

* https://github.com/wodby/elasticsearch#environment-variables
* https://github.com/wodby/kibana#environment-variables

## Changelog

This changelog is for Elasticsearch stack on Wodby, to see images changes see tags description on repository page: [elasticsearch](https://github.com/wodby/elasticsearch/releases) and [kibana](https://github.com/wodby/kibana/releases).

## 3.0.6

⬆️ Elasticsearch, Kibana 7.17.18

## 3.0.5

⬆️ Elasticsearch, Kibana 7.17.16

## 3.0.4

- ⬆️ Updated to 7.17.15
- 🪦 Version 6 has reached end of life

## 3.0.3

⬆️ Elasticsearch, Kibana 7.17.13

## 3.0.2

⬆️ Elasticsearch, Kibana 7.17.12

## 3.0.1

⬆️ Elasticsearch, Kibana 7.17.10

## 3.0.0

- ⚠️ This version of stack requires server infrastructure 6.0.0+
- ⬆️ Elasticsearch, Kibana 7.17.9

## 2.6.5

⬆️ Elasticsearch 7.17.8

## 2.6.4

⬆️ Elasticsearch, Kibana 7.17.7

## 2.6.3

⬆️ Kibana, Elasticsearch 7.17.6

### 2.6.2

⬆️ Elasticsearch, Kibana 7.17.5

### 2.6.1

⬆️ Elasticsearch, Kibana 7.17.4

### 2.6.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- 🏔 Alpine Linux updated to 3.15

### 2.5.26

⬆️ Elasticsearch, Kibana 7.17.2

### 2.5.25

⬆️ Elasticsearch, Kibana 7.17.1

### 2.5.24

⬆️ Elasticsearch, Kibana 7.17.0

### 2.5.23

⬆️ Elasticsearch, Kibana 7.16.3, 6.8.23

### 2.5.22

⬆️ Elasticsearch, Kibana 7.16.2, 6.8.22

### 2.5.21

🚨️ Elasticsearch, Kibana security updates 7.16.1, 6.8.21 [CVE-2021-44228 ](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q)

### 2.5.20

- 🚨 Fix for [CVE-2021-44228 ](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q)
- ⬆️ Updated to 7.16.0
- 🥶 Rebased to [wodby/openjdk](https://github.com/wodby/openjdk) with frozen Alpine 3.13
    
### 2.5.19

⬆️ Elasticsearch, Kibana 7.15.2

### 2.5.18

⬆️ Elasticsearch, Kibana 7.15.1, 6.8.20

### 2.5.17

⬆️&nbsp; Elasticsearch, Kibana 7.15.0, 6.8.19

### 2.5.16

⬆️&nbsp; Elasticsearch, Kibana 7.14.0, 6.8.18

### 2.5.15

⬆️&nbsp; Elasticsearch, Kibana 7.13.4, 6.8.17

### 2.5.14

⬆️&nbsp; Elasticsearch, Kibana 7.13.1

### 2.5.13

⬆️&nbsp; Elasticsearch, Kibana 7.13.0, 6.8.16

### 2.5.12

⬆️&nbsp; Elasticsearch, Kibana 7.12.1

### 2.5.11

⬆️&nbsp; Elasticsearch, Kibana 7.12.0, 6.8.15

### 2.5.10

⬆️&nbsp; Elasticsearch, Kibana 7.11.2

### 2.5.9

⬆️&nbsp; Elasticsearch, Kibana 7.11.1, 6.8.14

### 2.5.8

- ⬆️&nbsp; Elasticsearch, Kibana 7.10.1
- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 2.5.7

Elasticsearch, Kibana 7.10.0, 6.8.13

### 2.5.6

Elasticsearch, Kibana 7.9.2

### 2.5.5

Kibana, Elasticsearch 7.9.0, 6.8.12

### 2.5.4

Elasticsearch, Kibana 7.8.1, 6.8.11

### 2.5.3

Elasticsearch, Kibana 7.8.0

### 2.5.2

Elasticsearch, Kibana 7.7.1, 6.8.10

### 2.5.1

Elasticsearch, Kibana 7.6.2, 6.8.8

### 2.5.0

Elasticsearch, Kibana 7.5.0

### 2.4.6

Elasticsearch, Kibana 7.4.2, 6.8.5

### 2.4.5

Elasticsearch and Kibana 7.4.1, 6.8.4

### 2.4.4

Elasticsearch and Kibana 7.4.0, 6.8.3

### 2.4.3

Elasticsearch and Kibana updated to 7.3.1

### 2.4.2

Elasticsearch and Kibana updated to 7.3.0, 6.8.2

### 2.4.1

Bugfix: mixed up elasticsearch and kibana images

### 2.4.0

- Updated to 7.2.0
- We now install standard version of Elasticsearch and Kibana instead of OSS
- Base image for Elasticsearch changed to `adoptopenjdk/openjdk11`

### 2.2.3

Elasticsearch and Kibana updates: 7.1.1, 6.8.0

### 2.2.2

- Added new latest version 7.0
- Version 5.6 dropped (EOL)
- Updated to 6.7.2
- ES bugfix: multiple plugins installation failed https://github.com/wodby/elasticsearch/issues/1
- Added a few `$KIBANA_` env vars for basic configuration
- Alpine Linux updated to 3.9.4

### 2.2.1

- Elasticsearch and Kibana updated to 6.7.1
- Alpine Linux updated to 3.9.3

### 2.2.0

- Elasticsearch
    - Updated to 5.6.16
    - Added new version 6.7
    - Dropped all versions except latest 6.x and 5.x
    - Base image changed from `wodby/openjdk` to `wodby/alpine` 
- Kibana:
    - Updated to 5.6.16
    - Added new version 6.7
    - Dropped all versions except latest 6.x and 5.x
    - Base image changed from `wodby/openjdk` to `node`
    - We now use a specific node version requested by Kibana
    - Bugfix: Kibana 5.6 failed to start https://github.com/wodby/kibana/issues/1

### 2.1.4

Elasticsearch updated to 5.6.15

### 2.1.3

Elasticsearch and Kibana patch updates: 5.6.14

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
