You might have permissions issues caused by non-matching uid/gid on your host machine and the default user in php container.

### Linux

### macOS

[Use `-dev-macos` version](#macos-permissions-issues) of ruby image where default `wodby` user has `501:20` uid/gid that matches default macOS user.

### Windows

Since you [can't change owner of mounted volumes](https://github.com/docker/for-win/issues/39) in Docker for Win, the only solution is to run everything as root, add the following options to `ruby` service in your docker-compose file:

```yml
  ruby:
    user: root
```

### Different uid/gid?

You can rebuild the base image [wodby/ruby](https://github.com/wodby/ruby) with custom user/group ids by using docker build arguments `WODBY_USER_ID`, `WODBY_GROUP_ID` (both `1000` by default)
