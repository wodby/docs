# Service configs

Services can define configs that represent configuration files or config payloads overridden at stack or app level.

Unlike [settings](settings.md), configs are intended for larger or file-based configuration changes rather than a single value exposed through an environment variable.

Service configs are defined under the [`configs` section](template.md#configs) in a service template.

Each service config uses exactly one delivery mode:

- `helm`: Wodby sends the resolved config content into a Helm value. Use this when the chart creates and mounts the
  ConfigMap or Secret itself.
- `filepath`: Wodby creates a ConfigMap and mounts the file into the container at the specified path.
- `filename`: Wodby creates a ConfigMap entry but does not mount it. Use this when the chart expects an existing
  ConfigMap name and handles the mount on its own.

`config` can contain the file content inline or point to a file in the service repository.

If `processTokens: true` is set, Wodby resolves supported template tokens inside the effective config content before it
is passed to Helm or written into the generated ConfigMap. See [app tokens](../apps/tokens.md) for the public
built-in token list. Leave it disabled for configs that use their own `{{ ... }}` template syntax literally.

Stack and app overrides replace the config content or disable the config. They do not change the delivery mode defined
by the service template.
