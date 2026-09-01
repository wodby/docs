# Environment types

Environment types are Wodby's fixed deployment classifications. They are not organization-level records and cannot be
created, renamed, or deleted.

Choose a type directly when you create an [app environment](environments.md), managed database, cluster, or integration
policy. The same type is reused consistently for:

- stack and service configuration that differs by deployment stage
- cluster placement restrictions
- integration availability restrictions
- organization-level backup presets
- production-safe defaults and visual classification

The supported types are:

- `prod`
- `staging`
- `test`
- `dev`
- `feature`

An app environment still has its own permanent name, such as `production-eu` or `pr-123`. Its environment type is the
classification applied to that deployment. Multiple app environments may use the same type without creating another
organization-level object.

Use `prod` for live production workloads. Use `dev`, `staging`, `test`, and `feature` for their corresponding lifecycle
stages. Unless a stack explicitly defines different behavior, non-development types use production-safe runtime
settings.

## Compatibility

Older API fields and dashboard versions may refer to a named `Env` or environment ID. Those fields are deprecated.
Current integrations should send an `EnvType` value instead. Existing resources continue to work while clients migrate.
