# Key features

The key features of the Wodby platform:

* [Ready-to-run optimized infrastructure](#ready-to-run-optimized-infrastructure)
* [Instance management](#instance-management)
* [Bring your own server and git](#bring-your-own-server-and-git)
* [Integration with Vagrant](#integration-with-vagrant)
* [Remote Workspace and Debugging](#remote-workspace-and-debugging)
* [Team management](#team-management)
* [Free HTTPS via Let’s Encrypt](#free-https-via-lets-encrypt)
* [Backups with mirroring](#backups-with-mirroring)
* [Post-deployment scripts](#post-deployment-scripts)

## Ready-to-run optimized infrastructure

Wodby provides ready-to-run bundles for [Drupal](../infrastructure/bundles/drupal8/README.md) and [WordPress](../infrastructure/bundles/wordpress/README.md). Stacks consist of mandatory services (web server, database) and an optional services such as a search engine ([Apache Solr](../containers/apache-solr.html)) and Web database management (PhpMyAdmin). 

More pre-configured stacks are coming soon.

## Instance management

With Wodby you can easily deploy a new copy (dev, staging) to any server.

## Bring your own server and git

Wodby works with any hosting providers. Simply [connect your server](../servers/connecting-server/README.md) to Wodby from any cloud and deploy your apps. In the same fashion [bring your own git repository](../git/connecting-git/README.md) from any git provider.

## Integration with Vagrant

With Wodby you can streamline the entire workflow, not only dev > stage > prod, but also your local instance. [Connect your local Vagrant](../vagrant/README.md) to Wodby and deploy apps to your local machine. You can have as many apps on your machine as you want.

## Remote Workspace and Debugging

Sometimes there’s no point to use the local instance. In this case, you can connect to your remote server directly from your IDE. In other words, use [the remote workspace](../apps/remote-workspace/README.md). You can also save your time detecting bugs by debugging remotely any instance you want.

## Team management

As your developers team grows, it becomes hard to tell which developer is working on what project and it’s even harder to manage access to different projects. With Wodby, you can [onboard your entire team](../team/README.md) of developers and set roles with permissions to each employee per application.

## Free HTTPS via Let’s Encrypt

Almost every website has a sensitive information, such as login/password or credit card information. You should secure this information by using HTTPS protocol. Thanks to Let’s Encrypt now you <a href="../apps/domains.html#https-ssl-via-lets-encrypt">can get SSL certificates for free</a>. With Wodby you can enable HTTPS for your website in one click

## Backups with mirroring

Wodby offers both [automatic and manual backups](../apps/backups.md). This protects you against risk of losing sensitive data that is outside of regular version control systems (e.g. database, files). We also mirror your backups to a 3rd party secure and safe storage. By default Wodby provides 10GB storage on AWS S3.

## Post-deployment scripts

Developers often need to run some scripts such as run tests. You can automate this process by using our [post-deployment scripts](../deployment/post-deployment-scripts.md). Simply put wodby.yml file in your codebase and describe a deployment scenario in a very simple fashion.