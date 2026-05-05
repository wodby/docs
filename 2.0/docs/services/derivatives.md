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
