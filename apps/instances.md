# Application instance

When we say "application", we actually mean an application instance. By default we deploy development (or just dev) instance of the application. But you can create as many instances as you want.

You can remove or add a new instance from the `Instances` page. To get there navigate to the instance page and click on a cogwheel in the header.
 
## Instance type

There are four types of instances: local, dev, staging and production. The local instance can be deployed only to [Vagrant](../vagrant/README.md), it's also unique per user and not visible to other members of the organization.

The difference between the dev, staging and prod are:
 
* [Indexation rules for search robots](domains.md): do not index any domains (including custom) for dev and staging
* Error reporting level: display all errors on dev and none on staging and prod 
 