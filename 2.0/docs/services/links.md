# Service links

A service link describes how one service connects to another service.

One common example is an Nginx link to its upstream backend such as PHP-FPM.

Some links are mandatory and some are optional. If a link is mandatory, the stack must specify which other service satisfies it.

For example, in a Drupal stack the PHP service may require a `Database` link. That link can point either to a container-based `MariaDB` service or to an external cloud database service.

Service links are defined under the [`links` section](template.md#links) in a service template.
