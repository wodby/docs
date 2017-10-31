# Connecting Server to Wodby

## Requirements and recommendations

* Docker must not be installed (we need a specific version)
* Disabled or [configured](../../infrastructure/ufw.md) ufw
* The following ports must be free: `80` (http), `443` (https), `31222-32222` (containers)
* When external firewall used – open inbound ports `80` (http), `443` (https), `31222-32222`
* SWAP should either not exist (we set it automatically) or be a half as the size of RAM but in range 2 to 12 GB 
* Recommended minimum of server's RAM is **1GB**, Disk is **20GB**
* We strongly recommend to avoid connecting working servers

## Connection server from cloud provider

* [Amazon Web Services](/cloud/aws/README.md)
* [DigitalOcean](/cloud/digitalocean/README.md)
* [Linode](/cloud/linode/README.md)
* [Azure](/cloud/azure/README.md)
* [Google Cloud Platform](/cloud/gcp/README.md)
* [_Custom Cloud Provider_](/cloud/custom/README.md)
