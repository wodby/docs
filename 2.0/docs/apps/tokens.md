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

In addition to custom user-defined tokens, Wodby provides the following built-in tokens depending on context.

## `app`

### `app.id`

Application ID, not app-instance ID.

### `app.name`

Application machine name.

### `app.title`

Application title.

## `instance`

### `instance.id`

[App instance](instances.md) ID.

### `instance.name`

App-instance machine name.

### `instance.title`

App-instance title.

## `kubernetes`

### `kubernetes.id`

[Kubernetes cluster](../kubernetes/index.md) ID.

### `kubernetes.name`

Kubernetes cluster machine name.

### `kubernetes.externalID`

Kubernetes cluster external ID.

## `env`

### `env.id`

[Environment](env.md) ID.

### `env.name`

Environment machine name.

### `env.title`

Environment title.

### `env.type`

Environment type.

## `org`

### `org.id`

Organization ID.

## `service`

### `service.id`

App-service ID.

### `service.name`

App-service machine name.

### `service.title`

App-service title.

### `service.host`

App-service hostname.

### `service.image`

App-service image.

### `service.replicas`

App-service replica count.

## `database`

### `database.host`

[Database](../databases/index.md) hostname. This is private when accessed through an app service with a private database user, otherwise public.

### `database.port`

Database connection port. This is private when available, otherwise public.

### `database.driver`

Database driver, based on the database kind.

### `database.root.name`

Database superuser username.

### `database.root.password`

Database superuser password.

### `database.user`

Available when accessed through a database app service.

### `database.user.name`

Database username for the current app-service context.

### `database.user.password`

Database user password for the current app-service context.

### `database.db`

Available when accessed through a database app service.

### `database.db.name`

Database name for the current app-service context.

### `database.db.charset`

Database charset for the current app-service context.

### `database.db.collation`

Database collation for the current app-service context.

## `links`

Accessed as `links.[name].[token]`

### `links.[].host`

Linked app-service hostname.

### `links.[].port`

Primary port of the linked app service's primary endpoint.

### `links.[].env.[]`

Environment-variable value from the linked app service. Accessed as `links.[name].env.[env-var-name]`.

### `links.[].tokens.[]`

Token value from the linked app service. Accessed as `links.[name].tokens.[token-name]`.

### `links.[].database.[]`

Database token from the linked app service. Accessed as `links.[name].database.[database-token]`. See [`database`](#database) for the available database tokens.
