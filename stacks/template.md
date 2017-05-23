# Stack Template

You can create custom stacks by defining one via template or by forking stacks provided by Wodby. 

Stack template is a YML defining services, it's basically a simplified and limited version of [kubernetes schema](https://kubernetes.io/docs/resources-reference/v1.6/) in a format very close to docker compose.

> Stacks provided by Wodby (including forks) may have additional configurations not covered by templates. 
 
* [Service configuration reference](#service-configuration-reference)
    * [check-ready reference](#check-ready-reference)
    * [deployment reference](#deployment-reference)
    * [security_context reference](#security-context-reference)
* [Global volumes](#global-volumes)
* [Variable substitution](#variable-substitution)
* [Details](#details)
    * [memory](#memory)
    * [cpu](#cpu)
    * [ports](#ports)
* [Examples](#examples)
* [Permissions](#permissions)

## Service configuration reference

This section contains a list of all configuration options supported by a service definition.

| Name | Description | Mandatory | Schema | 
| ---- | ----------- | -------- | ------ |
| image | The image the container is running. | ✓ | string |
| entrypoint | Entrypoint string or array. The docker image’s ENTRYPOINT is used if this is not provided. |  | string, string array |
| command | Arguments to the entrypoint. The docker image’s CMD is used if this is not provided. |  | string, string array |
| working_dir | Container’s working directory. If not specified, the container runtime’s default will be used, which might be configured in the container image. |  | string |
| environment | List of environment variables to set in the container. |  | string array |
| volumes | Volumes to mount into the container’s filesystem. |  | string array |
| [memory](#memory) | Memory rules and limitations |  | int, string | 
| [cpu](#cpu) | CPU resources rules and limitations |  | int, string |
| [ports](#ports) | List of ports to expose from the container. |  | string array |
| [check_ready](#check-ready-reference) | Describes a health check to be performed against a container to determine whether it is alive or ready to receive traffic. |  | string array |
| [deployment](#deployment-reference) | Deployment enables declarative updates for services. |  | string array |
| [security_context](#security-context-reference) | Security context holds security configuration that will be applied to a container. |  | string array |

### check-ready reference

| Name | Description | Mandatory | Schema | 
| ---- | ----------- | --------- | ------ |
| exec | Exec specifies the action to take. | ✓ | command - array of strings |
| initial_delay_seconds | Number of seconds after the container has started before liveness probes are initiated. |  | int |
| period_seconds | How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. |  | int |
| failure_threshold | Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. | | int |
| success_threshold | Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Minimum value is 1.| | int |
| timeout_seconds | Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. | | int |

### deployment reference

| Name | Description | Mandatory | Schema | 
| ---- | ----------- | --------- | ------ |
| strategy | `rolling_update` or `recreate` (`rolling_update` by default). **Always use `recreate` strategy for stateful services like database and search engines.** |  | string |
| replicas | Number of desired containers. This is a pointer to distinguish between explicit zero and not specified. Defaults to 1. |  | int |
| min_ready_seconds | Minimum number of seconds for which a newly created service should be ready without any of its container crashing, for it to be considered available. Defaults to 0. |  | int |
| progress_deadline_seconds | The maximum time in seconds for a deployment to make progress before it is considered to be failed, not set by default. | | int |
| max_surge | The maximum number of containers that can be scheduled above the desired number of containers. Value must be an absolute number. Defaults to 1. | | int |
| max_unavailable | The maximum number of containers that can be unavailable during the update. Value must be an absolute number. Defaults to 1. | | int |

### security_context reference

| Name | Description | Mandatory | Schema | 
| ---- | ----------- | --------- | ------ |
| privileged | Run container in privileged mode. Processes in privileged containers are essentially equivalent to root on the host. |  | string |
| capabilities | The capabilities to add/drop when running containers. Defaults to the default set of capabilities granted by the container runtime. |  | array of strings |
| read_only_root_filesystem | Whether this container has a read-only root filesystem. Default is false. |  | string |
| run_as_non_root | Indicates that the container must run as a non-root user. If true, the Kubelet will validate the image at runtime to ensure that it does not run as UID 0 (root) and fail to start the container if it does. If unset or false, no such validation will be performed. |  | string |
| run_as_user | The UID to run the entrypoint of the container process. Defaults to user specified in image metadata if unspecified. |  | int |

## Global Volumes

You can define global volumes and use them in services under `volumes`. We recommend using `./` as a host path to mount volumes which is an equals `/srv/wodby/instances/<Instance UUID>`.

Example:

```yml
services:
    myapp:
        image: example/myapp
        ports:
            - 'edge::80/tcp'
        volumes:
            - 'docroot:/var/www'
            - 'db:/var/www'
volumes:
    docroot:
        path: ./docroot
    db:
        path: ./db
```

## Variable Substitution

You can define variables and substitute them in services under `environment`. 

Example:

```yml
services:
    backend:
        image: example/backend
        ports:
            - 'edge::80/tcp'
        environment:
            username: '%user'
            password: '%pass'

variables:
    user: 'admin'
    pass: 'auto:password:64'
```

## Details

### memory

You can specify memory limits and requests for a container in the following formats:   

```
128 - Request 128Mb of memory.
512:1024 - Request 512Mb of memory. Limit 1Gb of memory.
```

Limit is a maximum memory (in megabytes) available for a container. When a container exceeds this limit, it will be terminated (and automatically started again). Request defines how much memory must be available on a server to start this container (used in clusters).    

### cpu

You can specify CPU limits and requests for a container in the following formats:

```
1000 - Request 1 Core.
1500 - Request 1.5 Core.
650 - Request 0.65 Core.
200:250 - Request 0.2 Core. Limit 0.25 Core.
```
Minimum value is 100.

Limit is a # of CPU cores (1000 for 1 core) available for a container. When a container exceeds this limit, it will be terminated (and automatically started again). Request defines how many CPU cores must be available on a server to start this container (used in clusters).

### ports

Expose ports for a container in the format `[PUBLIC_PORT::BUNDLE_PORT:CONTAINER_PORT]`. 

Examples: 

* Map container's port 8080 to 80 for other containers within a stack.
```yml
services:
    backend:
        image: example/backend
        ports:
            - "80:8080"
``` 

* Same as "8080:8080"
```
"8080"
``` 

* Map 8080 to a public port within the range 31222-32222.   
```
"auto::8080"
```

* Map 8080 to a public port 80, `edge` is a reverse proxy handling 80 and 443 ports. A short technical domain `*.wod.by` will be generated for the first public port exposed via edge. 
```
"edge::8080"
```

* Map 8080 to a public 32223. 
```
"32223::8080"
```
  
* Map 8080 to 80 both public and within a stack.
```
"edge::80:8080"
```
    
* Map 8080 to 80 within a stack, assign public port automatically.
```
"auto::80:8080"
```

* Map 8080 to 80 within a stack, assign public port automatically.
```
"32223::80:8080"
```

## Examples

```yml
services:
    db:
        image: mysql
        environment:
            MYSQL_ROOT_PASSWORD: '%db_password'
        volumes:
            - './mysql:/var/lib/mysql'
        deployment:
            strategy: recreate            
    php:
        image: php
        environment:
            DB_USER: root
            DB_PASSWORD: '%db_password'
        memory: '512:1024'
        cpu: '900'
        security_context: 
            capabilities:
                add:    
                    - SYS_PTRACE
                drop:
                    - SYS_ADMIN
    nginx:
        image: nginx
        ports:
            - "edge::80:80"
variables:
    db_password: 'auto:password:64'
```

## Permissions

If you mount volumes from the server, the owner of the mounted directory in a container will be root (UID 0). This may cause issues because very often main process run from a different user. To avoid potential problems make sure you're either fixing volumes permissions in your container entrypoint script (recommended) or run the main process as root.  
