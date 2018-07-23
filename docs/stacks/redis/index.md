# Redis stack documentation

Redis can be configured with the following [environment variables](https://github.com/wodby/redis#environment-variables)

## Changelog

### 1.1.0

* Redis updated to 4.0.8
* Default [memory request](../config.md#resources) set to 256m
* Bugfix: redis 4 init could not disable THP on some servers

### 1.0.4

* Redis updated to 3.2.11, 4.0.2
* Fix init failure when there's no `/sys/kernel/mm/transparent_hugepage/enabled`
* Health check timeout increased to 30 seconds

### 1.0.3

* New experimental 4.0 version
* Update to 3.2.10
* Bugfix: incorrect data volume permissions
* Changed data volume location from `/var/lib/redis` to `/data`

### 1.0.2

* Set `net.core.somaxconn` to `65535` during initial start
* Transparent Huge Pages are now disabled to improve performance

### 1.0.1

* Version freeze https://github.com/wodby/redis#versions
* Redis now always has persistent volume

### 1.0.0

Initial release
