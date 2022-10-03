# Redis stack documentation

Redis can be configured with the following [environment variables](https://github.com/wodby/redis#environment-variables)

## Changelog

This changelog is for Redis stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/redis/releases).

### 1.6.3

⬆️ Redis 7.0.5

### 1.6.2

⬆️ Redis 7.0.4

### 1.6.1

⬆️ Redis 7.0.2

### 1.6.0

⭐️ Redis 7

### 1.4.1

⬆️ Redis 6.2.7

### 1.4.0

- ⬆️ Updated to 6.2.6, 5.0.14
- 🥶 Rebased to [wodby/base-redis](https://github.com/wodby/base-redis) with frozen Alpine 3.13

### 1.3.12

⬆️&nbsp; Alpine Linux freeze to 3.13

### 1.3.11

⬆️&nbsp; Redis 6.2.3

### 1.3.10

⬆️&nbsp; Redis 6.2.2

### 1.3.9

⬆️&nbsp; Redis 6.2.1, 5.0.12

### 1.3.8

⬆️&nbsp; Redis 6.2.0, 5.0.11

### 1.3.7

⬆️&nbsp; Base image Alpine Linux updated to 3.13.2

### 1.3.6

⬆️&nbsp; Redis 6.0.10

### 1.3.5

- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 1.3.4

Redis 6.0.9, 5.0.10

### 1.3.3

Redis 6.0.8

### 1.3.2

Redis 6.0.6

### 1.3.1

Redis 6.0.5

### 1.3.0

- Added redis 6
- Updated to 5.0.9
- Redis 4 now marked as EOL

### 1.2.9

Redis 5.0.8

### 1.2.8

Redis 5.0.7

### 1.2.7

Redis 3.1.3

### 1.2.6

Alpine Linux updated to 3.10.1

### 1.2.5

Redis updated to 5.0.5

### 1.2.4

Alpine Linux updated to 3.9.3

### 1.2.3

Redis updates: 5.0.4, 4.0.14

### 1.2.2

Redis updated to 4.0.13

### 1.2.1

Redis patch updates: 5.0.3, 4.0.12

### 1.2.0

Added Redis 5

### 1.1.1

Redis patch update: 4.0.11

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
