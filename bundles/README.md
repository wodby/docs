# Bundle

Bundle is a pre-configured infrastructure package for [your application](../apps/README.md). Every bundle consist of a few services, some of them are mandatory (backend, database), some of them are optional (cache storage, mail server, etc). Every service has at least one [container implementation](containers/README.md), e.g. for database services there's a MariaDB container. 

The following predefined bundles are currently available:

| Bundle | Current stable version |
| --------- | ----------------------------------- |
| [Drupal 8](drupal8.md)    | <a href="drupal8.html#331">3.3.1</a>   |
| [Drupal 7](drupal7.md)    | <a href="drupal7.html#331">3.3.1</a>   |
| [Drupal 6](drupal6.md)    | <a href="drupal6.html#331">3.3.1</a>   |
| [WordPress](wordpress.md) | <a href="wordpress.html#331">3.3.1</a> |

If you need a custom bundle please [contact our support team](../product/support.md). 

## Versioning

We regularly update bundles by releasing newer versions of bundles, such updates can include security updates and performance improvements.

You can find a bundle's version of your application on the list of your apps or under `Bundle` tab of your [instance](../apps/instances.md). If a bundle is outdated you will see an appropriate indicator. If you want perform the upgrade of your instances' bundles please [contact our support team](../product/support.md) to schedule the upgrade.
 
The bundle has a requirement for the minimal [version of infrastructure](../infrastructure/versioning.md) of the server where this bundle is deployed.
