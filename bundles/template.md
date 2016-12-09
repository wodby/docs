# Bundle Template

Bundle template is a YML defining services, it's similar to <a href="https://docs.docker.com/compose/compose-file/" target="_blank">docker compose</a> format but has a fewer options.

> Bundles provided by Wodby (including forks) may have additional configurations not covered by templates.
 
* [Service configuration reference](#service-configuration-reference)
* [Global volumes](#global-volumes)
* [Variable substitution](#variable-substitution)
* [Details](#details)
    * [memory](#memory)
    * [cpu](#cpu)
    * [ports](#ports)
* [Examples](#examples)

## Service configuration reference

This section contains a list of all configuration options supported by a service definition.

| Name | Description | Required | Schema | 
| ---- | ----------- | -------- | ------ |
| image | The image the container is running. | true | string |
| privileged | Run container in privileged mode. Processes in privileged containers are essentially equivalent to root on the host. | false | string |
| entrypoint | Entrypoint string or array. The docker image’s ENTRYPOINT is used if this is not provided. | false | string, string array |
| command | Arguments to the entrypoint. The docker image’s CMD is used if this is not provided. | false | string, string array |
| working_dir | Container’s working directory. If not specified, the container runtime’s default will be used, which might be configured in the container image. | false | string |
| [memory](#memory) | Memory rules and limitations | false | int, string | 
| [cpu](#cpu) | CPU resources rules and limitations | false | int, string |
| scale | The number of container replicas. Default is 1. | false | int |
| environment | List of environment variables to set in the container. | false | string array |
| volumes | Volumes to mount into the container’s filesystem. | false | string array |
| [ports](#ports) | List of ports to expose from the container. | false | string array |

## Global Volumes

You can define global volumes and use them in services under `volumes`. 

Example:

```yml
services:
    myapp:
        image: example/myapp
        ports:
            - 'edge::80/tcp'
    volumes:
        docroot: /var/www
        db: /var/www
volumes:
    docroot:
        path: /srv/wodby/docroot
    db:
        path: /srv/wodby/db
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
        username: %user
        password: %pass

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
100 - Request 1 Core.
150 - Request 1.5 Core.
100:200 - Request 1 Core. Limit 2 Cores.
```

Limit is a # of CPU cores (100 for 1 core) available for a container. When a container exceeds this limit, it will be terminated (and automatically started again). Request defines how many CPU cores must be available on a server to start this container (used in clusters).

### ports

Expose ports for a container in the format `[PUBLIC_PORT::BUNDLE_PORT:CONTAINER_PORT]`. 

Examples: 

* Map container's port 8080 to 80 for other containers within a bundle.
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
  
* Map 8080 to 80 both public and within a bundle.
```
"edge::80:8080"
```
    
* Map 8080 to 80 within a bundle, assign public port automatically.
```
"auto::80:8080"
```

* Map 8080 to 80 within a bundle, assign public port automatically.
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
    piwik:
        image: piwik
        environment:
            MYSQL_ROOT_PASSWORD: '%db_password'
        scale: 2
        memory: 512:1024
        cpu: 100
    nginx:
        image: nginx
        environment:
            MYSQL_ROOT_PASSWORD: '%db_password'
variables:
    db_password: 'auto:password:64'
```