# CLI reference

This reference is generated from the Wodby CLI command tree.

<a id="wodby"></a>

## `wodby`

CLI client for Wodby 2.0

### Options

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -h, --help                    help for wodby
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps
* [wodby backup](#wodby_backup)	 - Manage backups
* [wodby build](#wodby_build)	 - Manage app builds
* [wodby ci](#wodby_ci)	 - ci commands
* [wodby completion](#wodby_completion)	 - Generate the autocompletion script for the specified shell
* [wodby deployment](#wodby_deployment)	 - Manage deployments
* [wodby env](#wodby_env)	 - Manage environments
* [wodby import](#wodby_import)	 - Manage imports
* [wodby instance](#wodby_instance)	 - Manage app instances
* [wodby org](#wodby_org)	 - Manage organization context
* [wodby project](#wodby_project)	 - Manage projects
* [wodby route](#wodby_route)	 - Manage app routes
* [wodby task](#wodby_task)	 - Manage tasks
* [wodby version](#wodby_version)	 - Shows Wodby CLI version


<a id="wodby_app"></a>

## `wodby app`

Manage apps

### Options

```
  -h, --help            help for app
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby app get](#wodby_app_get)	 - Get app
* [wodby app instance](#wodby_app_instance)	 - Manage app instances
* [wodby app list](#wodby_app_list)	 - List apps
* [wodby app route](#wodby_app_route)	 - Manage app routes
* [wodby app service](#wodby_app_service)	 - Manage app services
* [wodby app status](#wodby_app_status)	 - Show app status


<a id="wodby_app_get"></a>

## `wodby app get`

Get app

```
wodby app get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps


<a id="wodby_app_instance"></a>

## `wodby app instance`

Manage app instances

### Options

```
  -h, --help            help for instance
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps
* [wodby app instance get](#wodby_app_instance_get)	 - Get app instance
* [wodby app instance list](#wodby_app_instance_list)	 - List app instances
* [wodby app instance status](#wodby_app_instance_status)	 - Show app instance status


<a id="wodby_app_instance_get"></a>

## `wodby app instance get`

Get app instance

```
wodby app instance get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app instance](#wodby_app_instance)	 - Manage app instances


<a id="wodby_app_instance_list"></a>

## `wodby app instance list`

List app instances

```
wodby app instance list [flags]
```

### Options

```
      --app string       App ID
      --cluster string   Cluster ID
      --cluster-app      Filter cluster app instances
  -h, --help             help for list
      --org string       Organization ID; inferred when current credentials expose one org
      --project string   Project ID or comma-separated project IDs
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app instance](#wodby_app_instance)	 - Manage app instances


<a id="wodby_app_instance_status"></a>

## `wodby app instance status`

Show app instance status

```
wodby app instance status ID [flags]
```

### Options

```
  -h, --help   help for status
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app instance](#wodby_app_instance)	 - Manage app instances


<a id="wodby_app_list"></a>

## `wodby app list`

List apps

```
wodby app list [flags]
```

### Options

```
      --cluster-app      Filter cluster apps
  -h, --help             help for list
      --org string       Organization ID; inferred when current credentials expose one org
      --project string   Project ID or comma-separated project IDs
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps


<a id="wodby_app_route"></a>

## `wodby app route`

Manage app routes

### Options

```
  -h, --help            help for route
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps
* [wodby app route create](#wodby_app_route_create)	 - Create app route
* [wodby app route delete](#wodby_app_route_delete)	 - Delete app route
* [wodby app route get](#wodby_app_route_get)	 - Get app route
* [wodby app route list](#wodby_app_route_list)	 - List app routes
* [wodby app route update](#wodby_app_route_update)	 - Update app route


<a id="wodby_app_route_create"></a>

## `wodby app route create`

Create app route

```
wodby app route create [flags]
```

### Options

```
      --action string      Route action: BACKEND or REDIRECT
      --data string        JSON request body
  -f, --file string        Path to JSON request body
  -h, --help               help for create
      --host string        Route host
      --letsencrypt        Request Let's Encrypt certificate
      --main               Make route the app instance main route
      --path string        Route path
      --path-type string   Route path type: PREFIX or EXACT
      --port int           Service port
      --primary            Make route primary for the service endpoint
      --service string     App service ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app route](#wodby_app_route)	 - Manage app routes


<a id="wodby_app_route_delete"></a>

## `wodby app route delete`

Delete app route

```
wodby app route delete ID [flags]
```

### Options

```
  -h, --help               help for delete
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
  -y, --yes                Confirm without prompting
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app route](#wodby_app_route)	 - Manage app routes


<a id="wodby_app_route_get"></a>

## `wodby app route get`

Get app route

```
wodby app route get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app route](#wodby_app_route)	 - Manage app routes


<a id="wodby_app_route_list"></a>

## `wodby app route list`

List app routes

```
wodby app route list [flags]
```

### Options

```
  -h, --help              help for list
      --instance string   App instance ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app route](#wodby_app_route)	 - Manage app routes


<a id="wodby_app_route_update"></a>

## `wodby app route update`

Update app route

```
wodby app route update ID [flags]
```

### Options

```
      --action string              Route action: BACKEND or REDIRECT
      --data string                JSON request body
      --disabled                   Set disabled state
  -f, --file string                Path to JSON request body
  -h, --help                       help for update
      --main                       Set main route state
      --path string                Route path
      --path-type string           Route path type: PREFIX or EXACT
      --primary                    Set primary route state
      --redirect-host string       Redirect host
      --redirect-path string       Redirect path
      --redirect-scheme string     Redirect scheme
      --redirect-status-code int   Redirect status code
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app route](#wodby_app_route)	 - Manage app routes


<a id="wodby_app_service"></a>

## `wodby app service`

Manage app services

### Options

```
  -h, --help            help for service
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps
* [wodby app service action](#wodby_app_service_action)	 - Run app service action
* [wodby app service get](#wodby_app_service_get)	 - Get app service
* [wodby app service list](#wodby_app_service_list)	 - List app services
* [wodby app service update](#wodby_app_service_update)	 - Update app service


<a id="wodby_app_service_action"></a>

## `wodby app service action`

Run app service action

```
wodby app service action ID ACTION [flags]
```

### Options

```
  -h, --help               help for action
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app service](#wodby_app_service)	 - Manage app services


<a id="wodby_app_service_get"></a>

## `wodby app service get`

Get app service

```
wodby app service get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app service](#wodby_app_service)	 - Manage app services


<a id="wodby_app_service_list"></a>

## `wodby app service list`

List app services

```
wodby app service list [flags]
```

### Options

```
  -h, --help              help for list
      --instance string   App instance ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app service](#wodby_app_service)	 - Manage app services


<a id="wodby_app_service_update"></a>

## `wodby app service update`

Update app service

```
wodby app service update ID [flags]
```

### Options

```
      --data string      JSON request body
      --disabled         Set disabled state
  -f, --file string      Path to JSON request body
  -h, --help             help for update
      --main             Set main service state
      --replicas int     Set replicas
      --version string   Set service version
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app service](#wodby_app_service)	 - Manage app services


<a id="wodby_app_status"></a>

## `wodby app status`

Show app status

```
wodby app status ID [flags]
```

### Options

```
  -h, --help   help for status
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app](#wodby_app)	 - Manage apps


<a id="wodby_backup"></a>

## `wodby backup`

Manage backups

### Options

```
  -h, --help            help for backup
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby backup create](#wodby_backup_create)	 - Create backup
* [wodby backup get](#wodby_backup_get)	 - Get backup
* [wodby backup list](#wodby_backup_list)	 - List backups


<a id="wodby_backup_create"></a>

## `wodby backup create`

Create backup

```
wodby backup create [flags]
```

### Options

```
      --bucket string          Storage bucket
      --data string            JSON request body
      --database-db string     Database DB ID
  -f, --file string            Path to JSON request body
  -h, --help                   help for create
      --integration int        Storage integration ID
      --name string            Backup name
      --service string         App service ID
      --storage-class string   Storage class
      --timeout duration       Maximum time to wait (default 10m0s)
      --wait                   Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby backup](#wodby_backup)	 - Manage backups


<a id="wodby_backup_get"></a>

## `wodby backup get`

Get backup

```
wodby backup get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby backup](#wodby_backup)	 - Manage backups


<a id="wodby_backup_list"></a>

## `wodby backup list`

List backups

```
wodby backup list [flags]
```

### Options

```
      --database string      Database ID
      --database-db string   Database DB ID
  -h, --help                 help for list
      --instance string      App instance ID
      --name string          Backup name
      --service string       App service ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby backup](#wodby_backup)	 - Manage backups


<a id="wodby_build"></a>

## `wodby build`

Manage app builds

### Options

```
  -h, --help            help for build
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby build deploy](#wodby_build_deploy)	 - Deploy build
* [wodby build get](#wodby_build_get)	 - Get build
* [wodby build list](#wodby_build_list)	 - List builds
* [wodby build registry-login](#wodby_build_registry-login)	 - Log Docker in to a build registry
* [wodby build void](#wodby_build_void)	 - Void build images


<a id="wodby_build_deploy"></a>

## `wodby build deploy`

Deploy build

```
wodby build deploy ID [flags]
```

### Options

```
  -h, --help               help for deploy
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby build](#wodby_build)	 - Manage app builds


<a id="wodby_build_get"></a>

## `wodby build get`

Get build

```
wodby build get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby build](#wodby_build)	 - Manage app builds


<a id="wodby_build_list"></a>

## `wodby build list`

List builds

```
wodby build list [flags]
```

### Options

```
  -h, --help              help for list
      --instance string   App instance ID
      --page int          Page number
      --page-size int     Page size
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby build](#wodby_build)	 - Manage app builds


<a id="wodby_build_registry-login"></a>

## `wodby build registry-login`

Log Docker in to a build registry

```
wodby build registry-login ID [flags]
```

### Options

```
  -h, --help          help for registry-login
      --host string   Docker registry host
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby build](#wodby_build)	 - Manage app builds


<a id="wodby_build_void"></a>

## `wodby build void`

Void build images

```
wodby build void ID [flags]
```

### Options

```
  -h, --help   help for void
  -y, --yes    Confirm without prompting
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby build](#wodby_build)	 - Manage app builds


<a id="wodby_ci"></a>

## `wodby ci`

ci commands

### Options

```
  -h, --help   help for ci
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby ci build](#wodby_ci_build)	 - Build images
* [wodby ci deploy](#wodby_ci_deploy)	 - Deploy build to Wodby
* [wodby ci init](#wodby_ci_init)	 - Initialize config for CI process
* [wodby ci release](#wodby_ci_release)	 - Push images
* [wodby ci run](#wodby_ci_run)	 - Run container


<a id="wodby_ci_build"></a>

## `wodby ci build`

Build images

```
wodby ci build [OPTIONS] [SERVICE]... [flags]
```

### Options

```
      --build-arg stringArray       Additional build argument in the 'NAME=VALUE' format. Repeatable
      --build-arg-env stringArray   Environment variable name to forward as a docker build argument. Repeatable
      --cache-backend string        Build cache backend: auto, local, registry, none (default "auto")
      --cache-dir string            Build cache directory for local backend
      --cache-from stringArray      Additional buildx cache source. Repeatable
      --cache-mode string           Build cache export mode (default "max")
      --cache-ref string            Build cache reference for registry backend
      --cache-to stringArray        Additional buildx cache destination. Repeatable
  -f, --dockerfile string           Relative path to dockerfile
      --from string                 Relative path to codebase (default ".")
  -h, --help                        help for build
      --to string                   Codebase destination path in container (default ".")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby ci](#wodby_ci)	 - ci commands


<a id="wodby_ci_deploy"></a>

## `wodby ci deploy`

Deploy build to Wodby

```
wodby ci deploy [SERVICE...] [flags]
```

### Options

```
  -h, --help               help for deploy
      --skip-post-deploy   Skip post deployment scripts execution
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby ci](#wodby_ci)	 - ci commands


<a id="wodby_ci_init"></a>

## `wodby ci init`

Initialize config for CI process

```
wodby ci init [OPTIONS] WODBY_APP_SERVICE_ID|WODBY_BUILD_ID [flags]
```

### Options

```
  -i, --build-id string   Custom build id (used if can't identify automatically)
  -n, --build-num int     Custom build number (used if can't identify automatically)
  -c, --context string    Build context (default: current directory)
      --dind              Use data container for sharing files between commands
      --fix-permissions   Fix codebase permissions explicitly. WARNING: this can change ownership of files in the project directory
  -h, --help              help for init
  -p, --provider string   Override detected build provider name
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby ci](#wodby_ci)	 - ci commands


<a id="wodby_ci_release"></a>

## `wodby ci release`

Push images

```
wodby ci release [SERVICE...] [flags]
```

### Options

```
  -b, --branch-tag             Additionally push tag with the current git branch name
  -h, --help                   help for release
  -l, --latest-branch string   Update latest tag when built from this branch (default "master")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby ci](#wodby_ci)	 - ci commands


<a id="wodby_ci_run"></a>

## `wodby ci run`

Run container

```
wodby ci run [OPTIONS] -s SERVICE | -i IMAGE [flags]
```

### Options

```
      --entrypoint string   Entrypoint
  -e, --env strings         Environment variables
      --env-file string     Env file
  -h, --help                help for run
  -i, --image string        Image
  -p, --path string         Working dir (relative path)
  -s, --service string      Service
  -u, --user string         User (defaults to current uid:gid for bind-mounted contexts, except 1000:1000)
  -v, --volume strings      Volumes
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby ci](#wodby_ci)	 - ci commands


<a id="wodby_completion"></a>

## `wodby completion`

Generate the autocompletion script for the specified shell

### Synopsis

Generate the autocompletion script for wodby for the specified shell.
See each sub-command's help for details on how to use the generated script.


### Options

```
  -h, --help   help for completion
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby completion bash](#wodby_completion_bash)	 - Generate the autocompletion script for bash
* [wodby completion fish](#wodby_completion_fish)	 - Generate the autocompletion script for fish
* [wodby completion powershell](#wodby_completion_powershell)	 - Generate the autocompletion script for powershell
* [wodby completion zsh](#wodby_completion_zsh)	 - Generate the autocompletion script for zsh


<a id="wodby_completion_bash"></a>

## `wodby completion bash`

Generate the autocompletion script for bash

### Synopsis

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

	source <(wodby completion bash)

To load completions for every new session, execute once:

#### Linux:

	wodby completion bash > /etc/bash_completion.d/wodby

#### macOS:

	wodby completion bash > $(brew --prefix)/etc/bash_completion.d/wodby

You will need to start a new shell for this setup to take effect.


```
wodby completion bash
```

### Options

```
  -h, --help              help for bash
      --no-descriptions   disable completion descriptions
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby completion](#wodby_completion)	 - Generate the autocompletion script for the specified shell


<a id="wodby_completion_fish"></a>

## `wodby completion fish`

Generate the autocompletion script for fish

### Synopsis

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

	wodby completion fish | source

To load completions for every new session, execute once:

	wodby completion fish > ~/.config/fish/completions/wodby.fish

You will need to start a new shell for this setup to take effect.


```
wodby completion fish [flags]
```

### Options

```
  -h, --help              help for fish
      --no-descriptions   disable completion descriptions
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby completion](#wodby_completion)	 - Generate the autocompletion script for the specified shell


<a id="wodby_completion_powershell"></a>

## `wodby completion powershell`

Generate the autocompletion script for powershell

### Synopsis

Generate the autocompletion script for powershell.

To load completions in your current shell session:

	wodby completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.


```
wodby completion powershell [flags]
```

### Options

```
  -h, --help              help for powershell
      --no-descriptions   disable completion descriptions
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby completion](#wodby_completion)	 - Generate the autocompletion script for the specified shell


<a id="wodby_completion_zsh"></a>

## `wodby completion zsh`

Generate the autocompletion script for zsh

### Synopsis

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

	source <(wodby completion zsh)

To load completions for every new session, execute once:

#### Linux:

	wodby completion zsh > "${fpath[1]}/_wodby"

#### macOS:

	wodby completion zsh > $(brew --prefix)/share/zsh/site-functions/_wodby

You will need to start a new shell for this setup to take effect.


```
wodby completion zsh [flags]
```

### Options

```
  -h, --help              help for zsh
      --no-descriptions   disable completion descriptions
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby completion](#wodby_completion)	 - Generate the autocompletion script for the specified shell


<a id="wodby_deployment"></a>

## `wodby deployment`

Manage deployments

### Options

```
  -h, --help            help for deployment
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby deployment create](#wodby_deployment_create)	 - Create deployment
* [wodby deployment get](#wodby_deployment_get)	 - Get deployment
* [wodby deployment list](#wodby_deployment_list)	 - List deployments
* [wodby deployment redeploy](#wodby_deployment_redeploy)	 - Redeploy deployment
* [wodby deployment wait](#wodby_deployment_wait)	 - Wait for deployment


<a id="wodby_deployment_create"></a>

## `wodby deployment create`

Create deployment

```
wodby deployment create [flags]
```

### Options

```
      --data string           JSON request body
  -f, --file string           Path to JSON request body
      --force                 Force service deployment
  -h, --help                  help for create
      --service stringArray   App service ID to deploy; repeatable
      --skip-post-deploy      Skip post-deployment scripts
      --skip-rollback         Skip rollback on failure
      --timeout duration      Maximum time to wait (default 10m0s)
      --wait                  Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby deployment](#wodby_deployment)	 - Manage deployments


<a id="wodby_deployment_get"></a>

## `wodby deployment get`

Get deployment

```
wodby deployment get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby deployment](#wodby_deployment)	 - Manage deployments


<a id="wodby_deployment_list"></a>

## `wodby deployment list`

List deployments

```
wodby deployment list [flags]
```

### Options

```
  -h, --help              help for list
      --instance string   App instance ID
      --page int          Page number
      --page-size int     Page size
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby deployment](#wodby_deployment)	 - Manage deployments


<a id="wodby_deployment_redeploy"></a>

## `wodby deployment redeploy`

Redeploy deployment

```
wodby deployment redeploy ID [flags]
```

### Options

```
  -h, --help               help for redeploy
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby deployment](#wodby_deployment)	 - Manage deployments


<a id="wodby_deployment_wait"></a>

## `wodby deployment wait`

Wait for deployment

```
wodby deployment wait ID [flags]
```

### Options

```
  -h, --help               help for wait
      --timeout duration   Maximum time to wait (default 10m0s)
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby deployment](#wodby_deployment)	 - Manage deployments


<a id="wodby_env"></a>

## `wodby env`

Manage environments

### Options

```
  -h, --help            help for env
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby env create](#wodby_env_create)	 - Create environment
* [wodby env delete](#wodby_env_delete)	 - Delete environment
* [wodby env get](#wodby_env_get)	 - Get environment
* [wodby env list](#wodby_env_list)	 - List environments
* [wodby env update](#wodby_env_update)	 - Update environment


<a id="wodby_env_create"></a>

## `wodby env create`

Create environment

```
wodby env create [flags]
```

### Options

```
      --data string    JSON request body
  -f, --file string    Path to JSON request body
  -h, --help           help for create
      --name string    Environment machine name
      --org string     Organization ID; inferred when current credentials expose one org
      --title string   Environment title
      --type string    Environment type: prod, staging, test, dev, or feature
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby env](#wodby_env)	 - Manage environments


<a id="wodby_env_delete"></a>

## `wodby env delete`

Delete environment

```
wodby env delete ID [flags]
```

### Options

```
  -h, --help               help for delete
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
  -y, --yes                Confirm without prompting
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby env](#wodby_env)	 - Manage environments


<a id="wodby_env_get"></a>

## `wodby env get`

Get environment

```
wodby env get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby env](#wodby_env)	 - Manage environments


<a id="wodby_env_list"></a>

## `wodby env list`

List environments

```
wodby env list [flags]
```

### Options

```
  -h, --help         help for list
      --org string   Organization ID; inferred when current credentials expose one org
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby env](#wodby_env)	 - Manage environments


<a id="wodby_env_update"></a>

## `wodby env update`

Update environment

```
wodby env update ID [flags]
```

### Options

```
      --data string    JSON request body
  -f, --file string    Path to JSON request body
  -h, --help           help for update
      --name string    Environment machine name
      --title string   Environment title
      --type string    Environment type: prod, staging, test, dev, or feature
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby env](#wodby_env)	 - Manage environments


<a id="wodby_import"></a>

## `wodby import`

Manage imports

### Options

```
  -h, --help            help for import
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby import create](#wodby_import_create)	 - Create import
* [wodby import get](#wodby_import_get)	 - Get import
* [wodby import list](#wodby_import_list)	 - List imports


<a id="wodby_import_create"></a>

## `wodby import create`

Create import

```
wodby import create [flags]
```

### Options

```
      --backup string        Backup ID
      --data string          JSON request body
      --database-db string   Database DB ID
  -f, --file string          Path to JSON request body
  -h, --help                 help for create
      --name string          Import name
      --service string       App service ID
      --source string        Import source
      --timeout duration     Maximum time to wait (default 10m0s)
      --url string           Import archive URL
      --wait                 Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby import](#wodby_import)	 - Manage imports


<a id="wodby_import_get"></a>

## `wodby import get`

Get import

```
wodby import get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby import](#wodby_import)	 - Manage imports


<a id="wodby_import_list"></a>

## `wodby import list`

List imports

```
wodby import list [flags]
```

### Options

```
      --database string      Database ID
      --database-db string   Database DB ID
  -h, --help                 help for list
      --instance string      App instance ID
      --service string       App service ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby import](#wodby_import)	 - Manage imports


<a id="wodby_instance"></a>

## `wodby instance`

Manage app instances

### Options

```
  -h, --help            help for instance
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby instance get](#wodby_instance_get)	 - Get app instance
* [wodby instance list](#wodby_instance_list)	 - List app instances
* [wodby instance status](#wodby_instance_status)	 - Show app instance status


<a id="wodby_instance_get"></a>

## `wodby instance get`

Get app instance

```
wodby instance get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby instance](#wodby_instance)	 - Manage app instances


<a id="wodby_instance_list"></a>

## `wodby instance list`

List app instances

```
wodby instance list [flags]
```

### Options

```
      --app string       App ID
      --cluster string   Cluster ID
      --cluster-app      Filter cluster app instances
  -h, --help             help for list
      --org string       Organization ID; inferred when current credentials expose one org
      --project string   Project ID or comma-separated project IDs
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby instance](#wodby_instance)	 - Manage app instances


<a id="wodby_instance_status"></a>

## `wodby instance status`

Show app instance status

```
wodby instance status ID [flags]
```

### Options

```
  -h, --help   help for status
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby instance](#wodby_instance)	 - Manage app instances


<a id="wodby_org"></a>

## `wodby org`

Manage organization context

### Options

```
  -h, --help            help for org
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby org current](#wodby_org_current)	 - Show organizations available to the current credentials


<a id="wodby_org_current"></a>

## `wodby org current`

Show organizations available to the current credentials

```
wodby org current [flags]
```

### Options

```
  -h, --help   help for current
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby org](#wodby_org)	 - Manage organization context


<a id="wodby_project"></a>

## `wodby project`

Manage projects

### Options

```
  -h, --help            help for project
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby project get](#wodby_project_get)	 - Get project
* [wodby project list](#wodby_project_list)	 - List projects


<a id="wodby_project_get"></a>

## `wodby project get`

Get project

```
wodby project get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby project](#wodby_project)	 - Manage projects


<a id="wodby_project_list"></a>

## `wodby project list`

List projects

```
wodby project list [flags]
```

### Options

```
  -h, --help         help for list
      --org string   Organization ID; inferred when current credentials expose one org
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby project](#wodby_project)	 - Manage projects


<a id="wodby_route"></a>

## `wodby route`

Manage app routes

### Options

```
  -h, --help            help for route
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby route create](#wodby_route_create)	 - Create app route
* [wodby route delete](#wodby_route_delete)	 - Delete app route
* [wodby route get](#wodby_route_get)	 - Get app route
* [wodby route list](#wodby_route_list)	 - List app routes
* [wodby route update](#wodby_route_update)	 - Update app route


<a id="wodby_route_create"></a>

## `wodby route create`

Create app route

```
wodby route create [flags]
```

### Options

```
      --action string      Route action: BACKEND or REDIRECT
      --data string        JSON request body
  -f, --file string        Path to JSON request body
  -h, --help               help for create
      --host string        Route host
      --letsencrypt        Request Let's Encrypt certificate
      --main               Make route the app instance main route
      --path string        Route path
      --path-type string   Route path type: PREFIX or EXACT
      --port int           Service port
      --primary            Make route primary for the service endpoint
      --service string     App service ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby route](#wodby_route)	 - Manage app routes


<a id="wodby_route_delete"></a>

## `wodby route delete`

Delete app route

```
wodby route delete ID [flags]
```

### Options

```
  -h, --help               help for delete
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
  -y, --yes                Confirm without prompting
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby route](#wodby_route)	 - Manage app routes


<a id="wodby_route_get"></a>

## `wodby route get`

Get app route

```
wodby route get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby route](#wodby_route)	 - Manage app routes


<a id="wodby_route_list"></a>

## `wodby route list`

List app routes

```
wodby route list [flags]
```

### Options

```
  -h, --help              help for list
      --instance string   App instance ID
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby route](#wodby_route)	 - Manage app routes


<a id="wodby_route_update"></a>

## `wodby route update`

Update app route

```
wodby route update ID [flags]
```

### Options

```
      --action string              Route action: BACKEND or REDIRECT
      --data string                JSON request body
      --disabled                   Set disabled state
  -f, --file string                Path to JSON request body
  -h, --help                       help for update
      --main                       Set main route state
      --path string                Route path
      --path-type string           Route path type: PREFIX or EXACT
      --primary                    Set primary route state
      --redirect-host string       Redirect host
      --redirect-path string       Redirect path
      --redirect-scheme string     Redirect scheme
      --redirect-status-code int   Redirect status code
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby route](#wodby_route)	 - Manage app routes


<a id="wodby_task"></a>

## `wodby task`

Manage tasks

### Options

```
  -h, --help            help for task
  -o, --output string   Output format: table or json (default "table")
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0
* [wodby task cancel](#wodby_task_cancel)	 - Cancel task
* [wodby task get](#wodby_task_get)	 - Get task
* [wodby task list](#wodby_task_list)	 - List tasks
* [wodby task logs](#wodby_task_logs)	 - Show task step logs
* [wodby task repeat](#wodby_task_repeat)	 - Repeat task
* [wodby task wait](#wodby_task_wait)	 - Wait for task


<a id="wodby_task_cancel"></a>

## `wodby task cancel`

Cancel task

```
wodby task cancel ID [flags]
```

### Options

```
  -h, --help               help for cancel
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
  -y, --yes                Confirm without prompting
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby task](#wodby_task)	 - Manage tasks


<a id="wodby_task_get"></a>

## `wodby task get`

Get task

```
wodby task get ID [flags]
```

### Options

```
  -h, --help   help for get
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby task](#wodby_task)	 - Manage tasks


<a id="wodby_task_list"></a>

## `wodby task list`

List tasks

```
wodby task list [flags]
```

### Options

```
      --app string        App ID
  -h, --help              help for list
      --instance string   App instance ID
      --org string        Organization ID
      --page int          Page number
      --page-size int     Page size
      --project string    Project ID or comma-separated project IDs
      --scope string      Task scope: project_and_org, org_only, or user_only
      --search string     Search query
      --statuses string   Comma-separated statuses
      --without-origin    Only tasks without origin
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby task](#wodby_task)	 - Manage tasks


<a id="wodby_task_logs"></a>

## `wodby task logs`

Show task step logs

```
wodby task logs ID [flags]
```

### Options

```
  -h, --help   help for logs
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby task](#wodby_task)	 - Manage tasks


<a id="wodby_task_repeat"></a>

## `wodby task repeat`

Repeat task

```
wodby task repeat ID [flags]
```

### Options

```
      --data string        JSON request body
  -f, --file string        Path to JSON request body
      --force              Force repeat
  -h, --help               help for repeat
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby task](#wodby_task)	 - Manage tasks


<a id="wodby_task_wait"></a>

## `wodby task wait`

Wait for task

```
wodby task wait ID [flags]
```

### Options

```
  -h, --help               help for wait
      --timeout duration   Maximum time to wait (default 10m0s)
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby task](#wodby_task)	 - Manage tasks


<a id="wodby_version"></a>

## `wodby version`

Shows Wodby CLI version

```
wodby version [flags]
```

### Options

```
  -h, --help   help for version
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby](#wodby)	 - CLI client for Wodby 2.0


