# Key features

The key features of the Wodby platform:

* [Ready-to-run infrastructure](#ready-to-run-infrastructure)
* [Instance management](#instance-management)
* [Bring your own server and git](#bring-your-own-server-and-git)
* [Regular updates](#regular-updates)
* [Integration with Vagrant](#integration-with-vagrant)
* [Remote Workspace and Debugging](#remote-workspace-and-debugging)
* [Team management](#team-management)
* [Free HTTPS via Let’s Encrypt](#free-https-via-lets-encrypt)
* [Backups](#backups)
* [Backups mirroring](#backups-mirroring)
* [Post-deployment scripts](#post-deployment-scripts)

## Ready-to-run infrastructure

Wodby provides pre-configured [bundles](../bundles/README.md) for [Drupal](../apps/drupal/README.md) and [WordPress](../apps/wordpress/README.md). All bundles are already optimized and need almost no additional configuration. Typical bundle looks like this:
  
| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../bundles/containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../bundles/containers/mariadb.md)            | ✓ |
| Cache storage         | [Redis](../bundles/containers/redis.md)                |   |
| Search engine         | [Solr](../bundles/containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../bundles/containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../bundles/containers/varnish.md)            | &nbsp; |

More bundles are coming soon.

## Instance management

Do you need a new copy (development, staging) of your app? With Wodby you can [deploy new copies of your app](../apps/instances.md) to any server in a few clicks. Copies have a complete environment consistency because they use the same [bundle](../bundles/README.md).  

## Bring your own server and git

Wodby works with any hosting providers. Simply [connect your server](../servers/README.md) to Wodby from any hosting provider and deploy your apps. In the same fashion [bring your own git repository](../git/README.md) from any git provider. You keep the control over your servers and the code.

## Regular updates 

We constantly improve the infrastructure we provide and regularly release [new versions of infrastructure](../infrastructure/versioning.md) and [bundles](../bundles/README.md). New versions include the latest improvements and security updates of components. 

## Integration with Vagrant

Streamline your entire workflow all the way to production by connecting your local machine to Wodby. [Connect your Vagrant box](../servers/connect/vagrant.md) to Wodby and deploy consistent copies of your apps to your local machine. 

## Remote Workspace and Debugging

Sometimes there’s no point to use the local instance. In this case, you can connect to your remote server directly from your IDE. In other words, use [the remote workspace](../apps/remote-workspace/README.md). You can also save your time detecting bugs by debugging remotely any instance you want.

## Team management

As your developers team grows, it becomes hard to tell which developer is working on what project and it’s even harder to manage access to different projects. With Wodby, you can [onboard your entire team](../team/README.md) of developers and set roles with permissions to each employee per application.

## Free HTTPS via Let’s Encrypt

Almost every website has a sensitive information, such as login/password or credit card information. You should secure this information by using HTTPS protocol. Thanks to Let’s Encrypt now you <a href="../apps/domains.html#https-ssl-via-lets-encrypt">can get SSL certificates for free</a>. With Wodby you can enable HTTPS for your website in one click

## Backups 

With Wodby you can be sure your applications' data is always safe. All applications deployed via Wodby have [automatic backups](../apps/backups.md) function. You can choose the time when you want to run the backup process to avoid extra load to your server. Additionally, choose for how long you want to store your backups to make sure your disk won't run out of space. 

## Backups mirroring

The main rule of backups is that you need at least two copies of them. That's why we <a href="../apps/backups.html#mirroring">mirror your backups</a> to a 3rd party secure and safe storage. You can connect your own 3rd party storage account or use AWS Simple Safe Storage (S3) account by Wodby with a 7 days depth.

## Post-deployment scripts

Deployment is not just `git pull`, very often it's a scenario that consists of scripts needed to run, such as running automated tests. You can automate this process by using our [post-deployment scripts](../deployment/post-deployment-scripts.md). Simply put wodby.yml file in your codebase and describe a deployment scenario in a very simple fashion by defining pipelines.