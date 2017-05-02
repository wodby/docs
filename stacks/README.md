# Stack

Stack is a pre-configured infrastructure package for [your application](../apps/README.md). Every stack consist of a few services (mandatory and optional). Every service has at least one [container implementation](containers.md), e.g. for database services there's a MariaDB container. 

Please visit [Stack Hub](https://cloud.wodby.com/#/hub/explore) to explore all the stacks.

## Stack documentation

* [Drupal 8](drupal8.md)
* [Drupal 7](drupal7.md)
* [Drupal 6](drupal6.md)
* [WordPress](wordpress.md)

## Template

You can create and edit stacks by modifying/defining [stack template](template.md).  

## Versioning

We regularly update stacks by releasing newer versions of stacks, such updates can include security updates and performance improvements.

You can find a stack's version of your application on the list of your apps or under `Stack` tab of your [instance](../apps/instances.md). If a stack is outdated you will see an appropriate indicator. If you want perform the upgrade of your instances' stacks please [contact our support team](../product/support.md) to schedule the upgrade.
 
The stack has a requirement for the minimal [version of infrastructure](../infrastructure/versioning.md) of the server where this stack is deployed.
