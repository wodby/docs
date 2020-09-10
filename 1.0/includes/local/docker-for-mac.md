There two major problems macOS users face with when using Docker for mac:

### macOS permissions issues

To avoid any permissions issues caused by different user id (uid), group id (gid) between your host and a container use `-dev-macos` version of php image (uncomment the environment variables in `.env` files) where the default user `wodby` has `501:20` uid/gid that matches default macOS user. 

### Bind mounts performance

By default, we use `:cached` option on bind mounts to improve performance on macOS (on Linux it behaves similarly to `consistent`). You can find more information about this in [docker blog](https://blog.docker.com/2017/05/user-guided-caching-in-docker-for-mac). However, there's the [synchronisation with Mutagen](https://mutagen.io/documentation/orchestration/projects) which is a [faster alternative](https://medium.com/netresearch/improving-performance-for-docker-on-mac-computers-when-using-named-volumes-55580efcbf68#bf1b).

#### Mutagen

The core idea of this project is to use an external volume that will sync your files with a file synchronizer tool.

```shell
brew install mutagen-io/mutagen/mutagen
```

1. Uncomment _Mutagen_ volume and service definitions in your compose file
2. Replace codebase _volumes_ definitions of services with the option below marked as "Mutagen"
3. Start the mutagen container `docker-compose up -d mutagen`
4. Start Mutagen: `mutagen project start -f mutagen/config.yml` (or just run `make mutagen` instead of steps 3 and 4)
5. Start other containers `docker-compose up -d` (or `make`)

Now when you change your code on the host machine Mutagen will sync your data to php and nginx/apache containers.

For more information visit [Mutagen project page](https://mutagen.io/).
