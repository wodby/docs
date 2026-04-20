# Service configs

Services can define configs that represent configuration files mounted into a service and overridden at stack or app
level.

Unlike [settings](settings.md), configs are intended for larger or file-based configuration changes rather than a
single value exposed through an environment variable.

Service configs are defined under the [`configs` section](template.md#configs) in a service template.
