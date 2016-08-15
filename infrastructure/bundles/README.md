# Bundle

Bundle is a pre-configured orchestratable set of [containers](../containers/README.md) for [the app](../../apps/README.md). Every application has its own bundle. You can think of a bundle as a representation of an app in the context of [the infrastructure provided by Wodby](../README.md).

The following bundles are currently available:

| Bundle | Current stable version |
| --------- | ----------------------------------- |
| [Drupal 8](drupal8.md)    | <a href="drupal8.html#330">3.3.0</a>   |
| [Drupal 7](drupal7.md)    | <a href="drupal7.html#330">3.3.0</a>   |
| [Drupal 6](drupal6.md)    | <a href="drupal6.html#330">3.3.0</a>   |
| [WordPress](wordpress.md) | <a href="wordpress.html#330">3.3.0</a> |

## Versioning

We regularly update bundles by releasing newer versions of bundles, such updates can include security updates and performance improvements.

You can find a bundle's version of your application on the list of your apps or under `Bundle` tab of your [instance](../../apps/instances.md). If a bundle is outdated you will see an appropriate indicator. If you want perform the upgrade of your instances' bundles please [contact our support team](../../product/support.md) to schedule the upgrade.
 
The bundle has a requirement for the minimal [version of infrastructure](../versioning.md) of the server where this bundle is deployed.
