# Derivative services

A derivative service reuses most of a parent service's configuration. Unlike [inheritance](template.md#from),
derivatives are additional services created from the parent, not reusable base templates.

For example, an `ssh` derivative of `php` can inherit the parent's environment variables and versions while overriding
its type, command, or endpoints.

Derivative services are defined under the [`derivatives` section](template.md#derivatives) in a service template.

Derivative names are prefixed with the service name. When a service inherits from another service with `from`, inherited
derivatives are renamed by replacing the base service prefix with the child service name. For example, if `drupal11-php`
inherits from `php`, the inherited `php-sshd` derivative is exposed as `drupal11-php-sshd`.

Stacks can still use a shorter stack service name for the derivative:

```yaml
services:
- name: php
  service: drupal11-php
  derivatives:
  - name: sshd
    service: drupal11-php-sshd
```

In this example, the stack service is named `sshd`, while `service` points to the actual derivative declared by the
referenced service.

## Rename a derivative

When a new version of a service renames a derivative, list the old name under `previousNames`:

```yaml
derivatives:
- name: php-jobs
  previousNames:
  - php-queue
  title: Jobs
  type: service
  args: ['php', 'artisan', 'queue:work']
```

Stacks that update to this service version keep their derivative stack service. Its stack-local name and the stack's
settings for it, such as replicas, environment variables, and Helm values, stay; only the derivative it runs changes.
App environments keep their app service too. Stack templates that still name the derivative by an old name in
`derivatives[].service` keep working.

Without `previousNames`, a renamed derivative counts as removed and replaced by a new one, and stacks lose their settings
for it.

Previous names must start with the service name and a dash, like derivative names. A previous name can't be the name of
another current derivative and can belong to only one derivative. When a service inherits from another service with
`from`, the previous names of inherited derivatives get the child service name as their prefix, like the derivative
names.
