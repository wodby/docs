# Requirements and recommendations for connected servers

* CPU architecture must be 64-bit
* [Supported OS](/servers/supported-os.md)
* Docker must not be installed (we require a specific version)
* Disabled or [configured](/infrastructure/ufw.md) ufw
* The following ports must be free: `80` (http), `443` (https), `31222-32222` (containers)
* When external firewall used – open inbound ports `80` (http), `443` (https), `31222-32222`
* SWAP should either not exist (we set it automatically) or be a half as the size of RAM but in range 2 to 12 GB 
* Recommended minimum of server's RAM is **1GB**, Disk is **20GB**
* We strongly recommend to avoid connecting working servers
