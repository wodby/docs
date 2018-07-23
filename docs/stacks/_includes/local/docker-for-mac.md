There two major problems macOS users face with when using Docker for mac:

### macOS permissions issues

To avoid any permissions issues caused by different user id (uid), group id (gid) between your host and a container use `-dev-macos` version of php image (uncomment the environment variables in `.env` files) where the default user `wodby` has `501:20` uid/gid that matches default macOS user. 

### Bind mounts performance

Out of the box Docker for mac bind mounts (volumes from host) have poor performance on sync. There are 2 ways how it can  be improved. [Performance tests 2017 Docker-sync vs Native](https://github.com/EugenMayer/docker-sync/wiki/Performance-Tests-2017).

#### User-guided caching

Since Docker for Mac 17.06 there's a new native `:cached` option available for bind mounts. You can find more information about this in [docker blog](https://blog.docker.com/2017/05/user-guided-caching-in-docker-for-mac).

Replace _codebase_ volume definition of _php_ and _nginx_/_apache_ services with the option below marked as "User-guided caching". 

#### Docker-sync

The core idea of this project is to use an external volume that will sync your files with a file synchronizer tool.

```bash
$ gem install docker-sync
```

1. Download `docker-sync.yml` file (inside of `docker4x.tar.gz` archive) from the latest stable release
2. Uncomment _docker-sync_ volume definition in your compose file
3. Replace _volumes_ definition of _php_ and _nginx_/_apache_ services with the option below marked as "Docker-sync".
4. Start docker-sync: `docker-sync start`
5. In a new shell run after you started docker-sync `docker-compose up -d`

Now when you change your code on the host machine docker-sync will sync your data to php and nginx/apache containers.

For more information visit [docker-sync project page](https://github.com/EugenMayer/docker-sync).
