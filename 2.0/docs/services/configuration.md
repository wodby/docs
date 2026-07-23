# Service configuration

Service configuration covers the values and generated resources that can be exposed from a service template and then
customized at stack or app-service level.

For the full manifest schema, see the [service template reference](template.md).

## Options

Options represent supported versions or deployment variants of a service.

A service can expose multiple options, and one of them can be marked as the default. Options can also carry an End of Life (EOL) date to show when upstream support ends.

Service options are defined under the [`options` section](template.md#options) in a service template.

### EOL flags

`EOL` means the selected service option has reached its end-of-life date. The service may still run, but upstream support
for that version has ended and you should plan to move to a supported option.

Wodby shows EOL flags in a few places:

- service version selectors and app-service version rows, when the selected version is EOL
- stack pages and stack lists, when an enabled stack service defaults to an EOL version
- app instance pages and app instance lists, when an enabled app service currently uses an EOL version

EOL checks use the latest service revision metadata available to Wodby. If a stack service or app service still points
to an older service revision, the dashboard can still mark the selected version as EOL, but the older revision may not
show the newest EOL date metadata or the newest non-EOL replacement versions in its version selector.

Update the stack service to the latest service revision before reviewing exact EOL dates or choosing a newer non-EOL
option. For app instances, publish the updated stack revision and upgrade the app instance; if needed, enable
`Update versions to default` during the app instance stack upgrade or change the app-service version afterward.

## Settings

Service settings are configurable service values exposed in the application form and in stack or app-level configuration.

In most cases, a setting maps to an environment variable or other service configuration value. Settings can also be reused by linked services when the service model supports that pattern.

Service settings are defined under the [`settings` section](template.md#settings) in a service template.

### Runtime and build scope

Settings are runtime values by default. A service template can mark a setting with:

- `runtime: false` to keep the setting out of deployed containers
- `build: true` to pass the setting-derived environment variable to CI builds as a Docker build argument

Use build-scoped settings when the service Dockerfile declares an `ARG` with the same name as the setting's `var`.
For example, a `docroot` setting with `var: DOCROOT_SUBDIR` should use `build: true` when the Dockerfile has
`ARG DOCROOT_SUBDIR`.

Changing a runtime-scoped setting marks the app service for redeploy. Changing a build-scoped setting marks it for
rebuild.

## Configs

Services can define configs that represent configuration files or config payloads overridden at stack or app level.

Unlike settings, configs are intended for larger or file-based configuration changes rather than a single value exposed
through an environment variable.

Service configs are defined under the [`configs` section](template.md#configs) in a service template.

Config names must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names), because Wodby may use them in generated ConfigMap names.

Each service config uses exactly one delivery mode:

- `helm`: Wodby sends the resolved config content into a Helm value. Use this when the chart creates and mounts the
  ConfigMap or Secret itself.
- `filepath`: Wodby creates a ConfigMap and mounts the file into the container at the specified path.
- `filename`: Wodby creates a ConfigMap entry but does not mount it. Use this when the chart expects an existing
  ConfigMap name and handles the mount on its own.

A config default can come from either:

- `config`: inline content or a file in the service repository.
- `default.source: image`: a file supplied by the service image for the selected service option.

Image-backed defaults let Wodby show the exact default for each service version without storing duplicate copies in the
service repository. The config's top-level `filepath` remains the destination for an override, while
`default.filepath` identifies the source file inside the image. Wodby resolves this content centrally for display; it
does not run a discovery job in your cluster.

When an image-backed config has no stack or app override, Wodby does not create or mount a ConfigMap for it. The
container continues to use the file supplied by its image. Resetting an override restores that behavior by deleting the
override rather than saving a copy of the displayed default.

The dashboard identifies whether a displayed default comes from the service repository or image. An image default can
temporarily appear as pending or unavailable while a newly published service revision is being resolved.

If `processTokens: true` is set, Wodby resolves supported template tokens inside the effective config content before it
is passed to Helm or written into the generated ConfigMap. See [app tokens](../apps/tokens.md) for the public
built-in token list. Leave it disabled for configs that use their own `{{ ... }}` template syntax literally.

Stack and app overrides replace the config content or disable the config. They do not change the delivery mode or
default source defined by the service template.

## Volumes

A service volume represents persistent storage used by a service.

Volumes can optionally be shared with other services. In that case, the volume must reference a link, and the linked
service provides the [distributed persistent storage](types.md#storage), for example through NFS, Rook, or Longhorn.

Service volumes can define a default size, which can then be overridden at the stack or app level.

When Wodby mounts a service volume directly, the volume must define `path` as the absolute mount path. This applies to
shared volumes and volumes that reuse storage from a linked service with `from`. Helm-managed volumes that are not
mounted directly by Wodby do not need `path`.

Service volumes are defined under the [`volumes` section](template.md#volumes) in a service template.

## Tokens

Service tokens are named text values defined by a service.

They can either:

- have a fixed value
- use a regular expression to generate a random secret value when the app is created or updated

Service tokens can be referenced from environment variables and other generated configuration.

Stacks can override service tokens. A stack-wide token overrides a service-defined token with the same name and
environment type, and a stack-service token overrides both for that specific stack service.

Built-in runtime tokens are documented in [app tokens](../apps/tokens.md), because they resolve in app-service
context and can be used from service, stack, and app configuration.

Service tokens are defined under the [`tokens` section](template.md#tokens) in a service template.

## Annotations

Services can define annotations that Wodby adds to Kubernetes resources when the underlying Helm chart supports extra annotations.

Service annotations are defined under the [`annotations` section](template.md#annotations) in a service template.

Annotations are Kubernetes resource metadata. They are not the same as app endpoint route settings. Use [route settings](../apps/endpoints.md#route-settings) for HTTP routing behavior such as HTTPS redirects, no-index headers, request body size, session affinity, and path rewrites.

## Certificates

Service certificates are self-signed certificates defined in service templates, not endpoint TLS certificates for
application routes. For managed endpoint certificates and organization-wide certificate inventory, see
[App endpoints](../apps/endpoints.md#tls-certificates).

Services can define self-signed certificates that are generated and then mounted into Kubernetes resources through Helm.

Service certificates are defined under the [`certs` section](template.md#certs) in a service template.

## Integrations

Services can declare which [Wodby integrations](../integrations/index.md) they support or require.

A common example is a mail service that connects to a third-party SMTP provider. External services can also use
integrations to connect to managed cloud services.

Service integrations are defined under the [`integrations` section](template.md#integrations) in a service template.
