# Can't connect a custom server

There are few known reasons for that:

* CPU architecture must be 64-bit
* Wodby's script must be run as a root
* Your server doesn't have enough RAM. the recommended minimum is 1GB
* Make sure your Linux distributive is supported with a compatible version. <a href="http://unix.stackexchange.com/questions/35183/how-do-i-identify-which-linux-distro-is-running" target="_blank">Learn how</a> to detect your distributive and the version
* A slow speed of Read/Write operations on a disk. See [the list](../servers/README.md) of recommended hosting providers
* Check your firewall settings and IP whitelist filter
* <a href="https://docs.docker.com/engine/installation/binaries/" target="_blank">Docker requirements</a> are not met 
* Required ports are not free: 80 (http), 443 (https), 31222-32222 (ssh)"


