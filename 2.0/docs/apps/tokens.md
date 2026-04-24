# Tokens

Tokens are named text values that can be referenced from environment variables and other generated configuration.

A token can either:

- have a fixed plain value
- use a regular expression to generate a random secret value when the app instance or app service is created or updated

In an app, token values are composed and overridden across several levels. Later levels override earlier ones:

1. service-defined tokens
2. stack-service tokens
3. stack-wide tokens
4. app-instance tokens
5. app-service tokens

This page is the public reference for built-in runtime tokens resolved in app-service context.

Some internal or infrastructure-only secret-bearing tokens are intentionally omitted from this public list.

## Where tokens are supported

Tokens are commonly supported in:

- environment variable values defined by services, stacks, apps, links, imports, and workloads
- Helm values such as `helm.values[].value` and other service manifest fields that feed values into a Helm chart
- config contents when `configs[].processTokens: true` is enabled
- action arguments, database actions, backup actions, and similar generated runtime configuration

## `app`

- `app.id`: application ID, not app-instance ID
- `app.name`: application machine name
- `app.title`: application title

## `instance`

- `instance.id`: [app instance](instances.md) ID
- `instance.name`: app-instance machine name
- `instance.namespace`: Kubernetes namespace for the app instance
- `instance.title`: app-instance title

## `kubernetes`

- `kubernetes.id`: [Kubernetes cluster](../kubernetes/index.md) ID
- `kubernetes.externalID`: cluster external ID
- `kubernetes.name`: cluster machine name
- `kubernetes.fullName`: cluster full name

Infrastructure-oriented FRPC tokens are also supported under `kubernetes.frpc.*`, but the secret-bearing/internal
subset is intentionally not documented here.

## `env`

- `env.id`: [environment](env.md) ID
- `env.name`: environment machine name
- `env.title`: environment title
- `env.type`: environment type

## `org`

- `org.id`: organization ID

## `service`

- `service.id`: app-service ID
- `service.name`: app-service machine name
- `service.title`: app-service title
- `service.host`: app-service hostname
- `service.fqdnPrefix`: generated host prefix used for domains
- `service.primaryURL`: primary URL for the service, including scheme when a primary domain exists
- `service.primaryHost`: primary domain name for the service
- `service.mainPort.number`: port number of the primary port on the primary endpoint
- `service.mainPort.protocol`: protocol of the primary port on the primary endpoint
- `service.replicas`: app-service replica count
- `service.secrets.env`: generated Kubernetes Secret name used for secret environment variables

Legacy `service.helm.release` is still supported for backward compatibility.

## `helm`

- `helm.release`: resolved Helm release name for the current app service

Use this token when a chart exposes labels, selectors, or values keyed by the Helm release name.

## `stack`

- `stack.id`: stack ID
- `stack.name`: stack machine name
- `stack.title`: stack title
- `stack.version`: stack version
- `stack.rev.id`: stack revision ID
- `stack.rev.number`: stack revision number

## `database`

Available when the current app-service context exposes a database.

- `database.host`: database hostname. This is private when accessed through an app service with a private database user, otherwise public
- `database.port`: database connection port. This is private when available, otherwise public
- `database.driver`: database driver, based on the database kind
- `database.root.name`: database superuser username
- `database.root.password`: database superuser password
- `database.user.name`: database username for the current app-service context
- `database.user.password`: database user password for the current app-service context
- `database.db.name`: database name for the current app-service context
- `database.db.charset`: database charset for the current app-service context
- `database.db.collation`: database collation for the current app-service context

## `links`

Accessed as `links.[name].[token]`.

- `links.[name].host`: linked app-service hostname
- `links.[name].port`: primary port of the linked app service's primary endpoint
- `links.[name].service.*`: service token from the linked app service. See [`service`](#service)
- `links.[name].instance.*`: app-instance token from the linked app service. See [`instance`](#instance)
- `links.[name].env.[env-var-name]`: environment-variable value from the linked app service
- `links.[name].tokens.[token-name]`: token value from the linked app service
- `links.[name].database.*`: database token from the linked app service. See [`database`](#database)

## `configs`

Accessed as `configs.[name].[token]`.

- `configs.[name].configMap`: generated Kubernetes ConfigMap name for the named config

## `volumes`

Accessed as `volumes.[name].[token]`.

- `volumes.[name].size`: effective volume size in GB
- `volumes.[name].claim`: generated PVC name for the named volume

## `integrations`

Accessed as `integrations.[name].[token]`.

- `integrations.[name].key`: integration key or secret value
- `integrations.[name].variables.[variable-name]`: exported integration variable by name
