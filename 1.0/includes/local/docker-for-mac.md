There three major problems macOS users face with when using Docker for mac:

### Platform performance
Apple's latest M1/M2 platforms should use images built for **arm64**, for example **linux/arm64**.

By default `docker compose up -d` will pull **amd64** images from Docker Hub. With these images your containers will run noticable slower, because of the platform mismatch.

Also if you visit `Images` section of your Docker Desktop, you will see warnings regarding some of the images being meant for AMD64 platform.

#### Fix the issue
While it is not possible to use **arm64** for all containers, it is possible to do so for most important ones.

Go to `docker-compose.yml` find `php` container definition. There add a new line `platform: linux/arm64`. So it looks like this:
```
  php:
    image: wodby/drupal-php:$PHP_TAG
    platform: linux/arm64
    container_name: "${PROJECT_NAME}_php"
    ...
```

Run `docker compose up -d`.

**Note:** You can do the same to `nginx` container. Unfortunatelly it is not possible with `mariadb`, `phpmyadmin`, etc. Becase those images are built only for **amd64** platform.

### macOS permissions issues

To avoid any permissions issues caused by different user id (uid), group id (gid) between your host and a container use `-dev-macos` version of php image (uncomment the environment variables in `.env` files) where the default user `wodby` has `501:20` uid/gid that matches default macOS user. 

### Bind mounts performance

By default, we use `:cached` option on bind mounts to improve performance on macOS (on Linux it behaves similarly to `consistent`). You can find more information about this in [docker blog](https://blog.docker.com/2017/05/user-guided-caching-in-docker-for-mac). However, there's the [synchronisation with Mutagen](https://mutagen.io/documentation/orchestration/projects) which is a [faster alternative](https://medium.com/netresearch/improving-performance-for-docker-on-mac-computers-when-using-named-volumes-55580efcbf68#bf1b).

#### Mutagen

The core idea of this project is to use an external volume that will sync your files with a file synchronizer tool.

First, we must install `mutagen` and `mutagen-compose`. Mutagen Compose requires Mutagen v0.13.0+. 

```shell
brew install mutagen-io/mutagen
brew install mutagen-io/mutagen/mutagen-compose
```

1. Modify your `docker-compose.yml` as following:
    - at the end of the file uncomment `x-mutagen:` and `volumes:` fields 
    - replace volumes definitions under services that needs to be synced with the ones marked as "Mutagen"
3. Make sure ids of `defaultOwner` and `defaultGroup` under `x-mutagen:` match ids of the image you're using, e.g. uid `501` and gid `20` for `-dev-macos` image by default
4. Start mutagen via `mutagen-compose up`

Now when you change your code on the host machine Mutagen will sync your data to containers that use the synced volumed.

For more information visit [Mutagen project page](https://mutagen.io/).
