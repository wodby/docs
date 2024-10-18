# Tokens

Tokens are text values that can have a plain value or a regular expression that will be used to generate a random secret value when an app services created/updated. Tokens can be used in environment variables' values.

In an app tokens compiled and overridden from different levels:

- Service defined tokens
- Stack service define tokens
- Stack-wide tokens
- App instance tokens
- App service tokens

In addition to custom user-defined Wodby provides the following tokens available depending on the context:

## `app`

### `app.id`

Application (not instance) ID.

### `app.name`

Application's machine name.

### `app.title`

Application's title.

## `instance`

### `instance.id`

[Application instance's](instances.md) ID.

### `instance.name`

Application instance's machine name

### `instance.title`

Application instance's title

## `kubernetes`

### `kubernetes.id`

[Kubernetes cluster's](../kubernetes/index.md) ID.

### `kubernetes.name`

Kubernetes cluster's machine name.

### `kubernetes.externalID`

Kubernetes cluster's external ID.

## `env`

### `env.id`

[Environment's](env.md) ID.

### `env.name`

Environment's machine name.

### `env.title`

Environment's title.

### `env.type`

Environment's type.

## `org`

### `org.id`

Organization's ID.

## `service`

### `service.id`

App service's ID.

### `service.name`

App service's machine name.

### `service.title`

App service's title.

### `service.host`

App service's hostname.

### `service.image`

App service's image.

### `service.replicas`

App service's number of replicas.

## `database`

### `database.host`

[Database's](../databases/index.md) hostname. Private host if access from app service with private user or public otherwise.

### `database.port`

Database's connection port. Private port if exists public otherwise.

### `database.driver`

Database's driver. Depends on the database kind.

### `database.root.name`

Database's superuser (root) username.

### `database.root.password`

Database's superuser (root) password.

### `database.user`

Available when accessed through a database app service.

### `database.user.name`

Current user's username.

### `database.user.password`

Current user's password.

### `database.db`

Available when accessed through a database app service.

### `database.db.name`

Current db's name.

### `database.db.charset`

Current db's charset.

### `database.db.collation`

Current db's collation.

## `links`

Accessed as `links.[name].[token]`

### `links.[].host`

Linked app service's hostname.

### `links.[].port`

Linked app service's primary endpoint's primary port.

### `links.[].env.[]`

Linked app service's environment variable value. Accessed as `links.[name].env.[env-var-name]`

### `links.[].tokens.[]`

Linked app service's token value. Accessed as `links.[name].tokens.[token-name]`

### `links.[].database.[]`

Linked app service's database token. Accessed as `links.[name].database.[database-token]`. See [`database`](#database) for database tokens.

