You might have permissions issues caused by non-matching uid/gid on your host machine and the default user in php container.

### Linux

Since version 5.0 the default php container user `wodby` has uid/gid `1000` that matches the default uid/gid for most popular Linux distributions.  

### macOS

[Use `-dev-macos` version](#macos-permissions-issues) of php image where default `wodby` user has `501:20` uid/gid that matches default macOS user.

### Windows

Since you [can't change owner of mounted volumes](https://github.com/docker/for-win/issues/39) in Docker for Win, the only solution is to run everything as root, add the following options to `php` service in your docker-compose file:

```yml
  php:
    user: root
    command: "php-fpm -R"
    environment:
      PHP_FPM_USER: root
      PHP_FPM_GROUP: root
```

### Different uid/gid?

You can rebuild the base image [wodby/php](https://github.com/wodby/php) with custom user/group ids by using docker build arguments `WODBY_USER_ID`, `WODBY_USER_ID` (both `1000` by default)
