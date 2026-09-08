# Stack template

Create a custom stack by writing a YAML template or by forking a stack provided
by Wodby. The format is a deliberately limited deployment schema inspired by
Docker Compose and Kubernetes; arbitrary fields from either format are not
accepted.

!!! note "Managed-stack features"
    Managed stacks and their forks can contain implementation catalog data and
    upgrade behavior that cannot be expressed in a custom template.

## Top-level sections

| Name | Required | Description |
| --- | --- | --- |
| `services` | yes | Named container services. |
| `variables` | no | Reusable literal or generated values. |
| `volumes` | no | Named persistent host-path volumes. |
| `service_types` | no | Display names for service categories referenced by a service's `type`. |
| `metadata` | no | Stack metadata retained with the template. |

Names of services and volumes can contain lowercase letters, numbers, and
hyphens. Variable names can contain lowercase letters, numbers, and
underscores.

## Service reference

| Name | Type | Description |
| --- | --- | --- |
| `image` | string | Required container image reference. |
| `image_pull` | string | `Always` or `IfNotPresent`; defaults to the runtime policy used by Wodby. |
| `entrypoint` | string or string array | Replaces the image entrypoint. |
| `command` | string or string array | Arguments passed to the entrypoint, replacing the image command. |
| `working_dir` | string | Container working directory. |
| `environment` | map | Environment variable names and string or numeric values. |
| `volumes` | string array | Host or named-volume mounts. Add `:ro` for a read-only mount. |
| [`memory`](#memory) | integer or string | Memory request and optional limit in MB. |
| [`cpu`](#cpu) | integer or string | CPU request and optional limit in millicores. |
| [`ports`](#ports) | string array | Internal and public port mappings. |
| [`check_ready`](#readiness-and-liveness-checks) | map | Readiness probe used to decide when the service can receive traffic. |
| [`check_alive`](#readiness-and-liveness-checks) | map | Liveness probe used to decide when a container should be restarted. |
| [`deployment`](#deployment) | map | Replica, update-strategy, and deployment-source settings. |
| [`security_context`](#security-context) | map | Container privilege and user settings. |
| `annotations` | map | Annotations applied to the rendered workload. |
| `metadata` | map | String or numeric service metadata. |
| `title` | string | Human-readable service title. |
| `type` | string | Service category, optionally declared under `service_types`. |
| `enabled` | boolean | Whether the service is initially enabled; defaults to `true`. |
| `required` | boolean | Prevents the service from being disabled when `true`; defaults to `false`. |
| `scale` | integer | Legacy replica field. Prefer `deployment.replicas`. |
| `privileged` | boolean | Legacy privilege field. Prefer `security_context.privileged`. |

### Memory

Specify a request alone or a request and limit separated by a colon:

```yaml
memory: 128       # request 128 MB
memory: 512:1024  # request 512 MB, limit 1024 MB
```

The limit cannot be lower than the request. A request reserves scheduling
capacity; it is not a measurement of current use. Exceeding the memory limit
can terminate the container with an out-of-memory error. Infrastructure 7 does
not use swap.

### CPU

CPU values use millicores, where `1000` is one core. The minimum request is
`100`:

```yaml
cpu: 1000      # request 1 core
cpu: 650       # request 0.65 core
cpu: 200:250   # request 0.2 core, limit 0.25 core
```

The limit cannot be lower than the request. Kubernetes throttles a container
that reaches its CPU limit; it does not terminate the container merely for
using its full CPU allowance.

### Ports

Port entries use:

```text
[PUBLIC_PORT::][SERVICE_PORT:]CONTAINER_PORT[/tcp|udp]
```

TCP is used when the protocol is omitted.

```yaml
ports:
  - "8080"               # service and container port 8080
  - "80:8080"            # service port 80 to container port 8080
  - "edge::80:8080"      # publish HTTP through Edge
  - "auto::8080"         # allocate a stable node port
  - "32223::80:8080"     # use an explicit unmanaged node port
  - "32767::5353/udp"    # explicit UDP node port
```

`auto` allocates a port from Wodby's managed range, 31222–32222. An explicit
node port must be in the separate unmanaged range, 32223–32767. Open the
selected port in any external firewall. `edge` publishes the service through
the Wodby edge proxy; the first Edge-published service receives a technical
domain.

### Readiness and liveness checks

Both `check_ready` and `check_alive` accept exactly one action: `exec` or
`http`.

```yaml
check_ready:
  exec:
    command: ["/bin/sh", "-c", "test -f /tmp/ready"]
  initial_delay_seconds: 5
  period_seconds: 10
  timeout_seconds: 2
  failure_threshold: 3
  success_threshold: 1
```

For an HTTP probe:

```yaml
check_alive:
  http:
    path: /health
    port: 8080
    scheme: HTTP
    headers:
      X-Health-Check: wodby
  initial_delay_seconds: 10
  period_seconds: 20
```

HTTP `path` and `port` are required. `host`, `scheme`, and `headers` are
optional. Probe timing fields use seconds; periods, thresholds, and timeouts
must be positive, while the initial delay can be zero.

### Deployment

| Name | Type | Description |
| --- | --- | --- |
| `strategy` | string | `rolling_update` (default) or `recreate`. |
| `replicas` | integer | Desired replicas, including explicit zero; defaults to one. |
| `min_ready_seconds` | integer | Time a new replica must remain ready before becoming available. |
| `progress_deadline_seconds` | integer | Maximum time for a deployment to make progress. |
| `max_surge` | integer | Replicas allowed above the desired count during a rolling update. |
| `max_unavailable` | integer | Replicas allowed to be unavailable during a rolling update. |
| `type` | string | `ci` for CI-built code or `git` for direct Git deployment. |

Use `recreate` for stateful services such as databases and search engines.
Rolling updates can run old and new replicas simultaneously and therefore
require storage and application behavior designed for concurrent replicas.

A service with `deployment.type: ci` starts with zero replicas until its first
CI build is deployed. See [Code deployment](../apps/deploy.md#cicd).

### Security context

| Name | Type | Description |
| --- | --- | --- |
| `privileged` | boolean | Gives the container host-equivalent privileges. Avoid unless required. |
| `capabilities.add` | string array | Linux capabilities to add. |
| `capabilities.drop` | string array | Linux capabilities to remove. |
| `read_only_root_filesystem` | boolean | Mounts the container root filesystem read-only. |
| `run_as_non_root` | boolean | Rejects an image that would run as UID 0. |
| `run_as_user` | integer | UID used to run the container process. |

Example:

```yaml
security_context:
  run_as_non_root: true
  run_as_user: 1000
  read_only_root_filesystem: true
  capabilities:
    drop: ["ALL"]
```

## Volumes

Define a host-path volume once and mount it into one or more services:

```yaml
volumes:
  application-data:
    path: ./data

services:
  application:
    image: example/application:1
    volumes:
      - "application-data:/var/lib/application"
      - "./configuration:/etc/application:ro"
```

A relative host path is resolved beneath the instance data directory,
`/srv/wodby/instances/INSTANCE_UUID`. The mount suffix `:ro` makes that service
mount read-only.

Custom-template global volumes are currently materialized as host paths. Mount
external storage such as NFS on the server first and reference its host path;
do not rely on a template-level NFS driver.

Mounted host directories are commonly created as root. Make sure the image's
runtime UID can read or write them as needed, preferably through an idempotent
entrypoint permission check rather than running the main process as root.

## Variables and generated values

Variables can be literal values or generated once when Wodby creates the stack
revision:

```yaml
variables:
  db_user: application
  db_password: auto:password:64
  application_key: auto:openssl_rand:32:base64
  hex_key: auto:openssl_rand:32:hex
```

`auto:password:LENGTH` creates a password of the requested length.
`auto:openssl_rand:LENGTH:ENCODING` creates random bytes encoded as `base64` or
`hex`; the default length is 32 bytes and the default encoding is `base64`.

Reference a variable with Mustache syntax:

```yaml
services:
  application:
    image: example/application:1
    environment:
      DB_USER: "{{db_user}}"
      DB_PASSWORD: "{{db_password}}"
      APP_KEY: "base64:{{application_key}}"
```

The older `%db_password` form remains supported for compatibility, but new
templates should use `{{db_password}}`. Write `%%` when a literal percent sign
would otherwise be interpreted as a legacy variable token.

Environment entries that still reference generated password material are
protected by Wodby. See
[Protected and generated values](config.md#protected-and-generated-values).

## Complete example

```yaml
service_types:
  database: Database
  web: Web

variables:
  db_password: auto:password:64

volumes:
  database-data:
    path: ./database

services:
  database:
    title: Database
    type: database
    image: mariadb:11
    required: true
    environment:
      MARIADB_ROOT_PASSWORD: "{{db_password}}"
    volumes:
      - "database-data:/var/lib/mysql"
    deployment:
      strategy: recreate
    check_ready:
      exec:
        command: ["healthcheck.sh", "--connect"]

  web:
    title: Web
    type: web
    image: example/web:1
    ports:
      - "edge::80:8080"
    environment:
      DB_PASSWORD: "{{db_password}}"
    memory: "256:512"
    cpu: "200:500"
    deployment:
      strategy: rolling_update
      replicas: 1
```
