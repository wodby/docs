# Derivative services

A derivative service reuses most of a parent service's configuration. Unlike [inheritance](template.md#from),
derivatives are additional services created from the parent, not reusable base templates.

For example, an `ssh` derivative of `php` can inherit the parent's environment variables and versions while overriding
its type, command, or endpoints.

Derivative services are defined under the [`derivatives` section](template.md#derivatives) in a service template.
