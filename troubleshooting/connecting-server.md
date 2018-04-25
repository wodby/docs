# Can't connect server

There are few known reasons for that:

* Make sure your server satisfies [requirements and recommendations](/servers/requirements.md)
* Wodby's script must be run as a root
* A slow speed of Read/Write operations on a disk. See [the list](/servers/connect/README.md) of recommended hosting providers
* [Docker requirements](https://docs.docker.com/engine/installation/binaries/) are not met 
* [ufw enabled](/infrastructure/ufw.html)
* Inbound / outbound external firewall
* Non-compatible virtualization (virtuozza)
