# App deployment failed due to timeout

This error means that one of the deployment steps exceeded its timeout. There are few known reasons for that:

* Your server doesn't have enough RAM. the recommended minimum is 1GB
* Internet connection is too slow, we download packages 
* A slow speed of Read/Write operations on a disk. See [the list](../servers/connecting-server/README.md) of recommended hosting providers
