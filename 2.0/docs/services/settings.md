# Service settings

Service settings are configurable service values exposed in the application form and in stack or app-level configuration.

In most cases, a setting maps to an environment variable or other service configuration value. Settings can also be reused by linked services when the service model supports that pattern.

Service settings are defined under the [`settings` section](template.md#settings) in a service template.

## Runtime and build scope

Settings are runtime values by default. A service template can mark a setting with:

- `runtime: false` to keep the setting out of deployed containers
- `build: true` to pass the setting-derived environment variable to CI builds as a Docker build argument

Use build-scoped settings when the service Dockerfile declares an `ARG` with the same name as the setting's `var`.
For example, a `docroot` setting with `var: DOCROOT_SUBDIR` should use `build: true` when the Dockerfile has
`ARG DOCROOT_SUBDIR`.

Changing a runtime-scoped setting marks the app service for redeploy. Changing a build-scoped setting marks it for
rebuild.
