# Docker registry stack documentation

Add the following environment variables to use redis for layer metadata cache:
```
REGISTRY_STORAGE_CACHE_BLOBDESCRIPTOR: redis
REGISTRY_REDIS_ADDR: redis:6379
REGISTRY_REDIS_PASSWORD: [YOUR REDIS PASSWORD]
```

You can acquire auto-generated redis password from `App > Stack > Redis` page.

## Changelog

### 0.1.2

Added Redis 5

### 0.1.1

* Default [memory request](../config.md#resources) set to 8m

### 0.1.0

Initial release
