# Stack

Stack is a pre-configured infrastructure package for [your application](../apps/README.md). Every stack consist of a few services, some of them are mandatory (backend, database), some of them are optional (cache storage, mail server, etc). Every service has at least one [container implementation](containers/README.md), e.g. for database services there's a MariaDB container. 

The following predefined stacks are currently available:

| Stack | Current stable version |
| ------ | ---------------------- |
| [Drupal 8](drupal8.md) | v3.3.1 |
| [Drupal 7](drupal7.md) | v3.3.1 |
| [Drupal 6](drupal6.md) | v3.3.1 |
| [WordPress](wordpress.md) | v3.3.1 |
| [Apache Solr 5.5](solr.md) | N/A |
| [Apache Solr 6.3](solr.md) | N/A |
| [Custom stacks](custom/README.md) | N/A | 

## Template

You can create and edit stacks by modifying/defining [stack template](template.md).  

## Versioning

We regularly update stacks by releasing newer versions of stacks, such updates can include security updates and performance improvements.

You can find a stack's version of your application on the list of your apps or under `Stack` tab of your [instance](../apps/instances.md). If a stack is outdated you will see an appropriate indicator. If you want perform the upgrade of your instances' stacks please [contact our support team](../product/support.md) to schedule the upgrade.
 
The stack has a requirement for the minimal [version of infrastructure](../infrastructure/versioning.md) of the server where this stack is deployed.
