# Connecting server to Wodby

## Instructions

Before connecting your server to Wodby please make sure it satisfies [requirements and recommendations](#requirements-and-recommendations)

* [Amazon Web Services](../integrations/aws.md)
* [DigitalOcean](../integrations/digitalocean.md)
* [Azure](../integrations/azure.md)
* [Google Cloud Platform](../integrations/gcp.md)
* [_Custom Cloud Provider_](../integrations/custom.md)

## Requirements and recommendations

* CPU architecture must be 64-bit
* [Supported OS](#supported-os)
* Docker must not be installed (we require a specific version)
* Disabled or configured ufw
* The following ports must be free: 80 (http), 443 (https), 31222-32222 (containers)
* When external firewall used – open inbound ports 80 (http), 443 (https), 31222-32222
* SWAP should either not exist (we set it automatically) or be a half as the size of RAM but in range 2 to 12 GB
* Recommended minimum of server's RAM is 1GB, Disk is 20GB
* We strongly recommend to avoid connecting working server

## Supported OS

Wodby supports the following Linux distributions (x64 only):

* Debian 11 bullseye (recommended)
* Debian 10 buster
* Debian 9 stretch
* Ubuntu 20.04 LTS

[Learn how](http://unix.stackexchange.com/questions/35183/how-do-i-identify-which-linux-distro-is-running) to detect your distributive and the versions

## Proxy support

Since version 5.9.2 the installer and Wodby agent support proxy. For installer all is needed is to have `$HTTP_PROXY` environment variable on the host machine. After the installation (and optionally a reboot), you will need to patch the wodby agent to pass through the `HTTP_PROXY` (as `WODBY_HTTP_PROXY`) environment variable from the host machine:
```
kubectl patch deployment agent -n wodby -p '{"spec":{"template":{"spec":{"containers":[{"env":[{"name":"WODBY_HTTP_PROXY","value":"'$(echo $HTTP_PROXY)'"}],"name":"agent"}]}}}}'
```

## Uninstall

To uninstall Wodby's infrastructure (5.x) from your server simply execute following command as root:

```shell
wodby uninstall
```
