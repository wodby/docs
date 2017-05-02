# Connecting Server to Wodby

Wodby supports the following options for connecting a server:

| Hosting provider | [Native integration](../../integrations/README.md) |
| ---------------- | --------------------------------------------------- |
| [Any](custom.md) |  |
| [DigitalOcean](do.md) | ✓ |
| [AWS](aws.md) | |
| [Google Cloud Platform (GCP)](gcp.md) | |
| [Linode](linode.md) | |
| [Microsoft Azure](azure.md) | |
| [Vagrant](vagrant.md) | |
| Rackspace | &nbsp; |

## Recommendations when connecting a server

* Docker must not be installed (we need a specific version)
* Disabled or [configured](../../infrastructure/ufw.md) ufw
* Recommended minimum of server's RAM is 1GB
* We strongly recommend to avoid connecting working servers
* The following ports must be free: 80 (http), 443 (https), 31222-32222
* When external firewall used – open inbound ports 80 (http), 443 (https), 31222-32222
