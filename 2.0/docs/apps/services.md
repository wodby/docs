# Application Services

## Overview

```mermaid
flowchart TD
    subgraph APP["<div style='margin-top:10px; white-space: nowrap;'>App Instance (e.g. production)</div>"]
        subgraph sapp[ ]
            direction LR
            app1["app service"]
            app2["app service"]
            appEllipsis["..."]
            app3["app service"]
        end
        style sapp fill:none,stroke:none,stroke-width:0px
    end

    subgraph SR["<div style='margin-top:10px; white-space: nowrap;'>Stack Revision</div>"]
        subgraph sstack[ ]
            direction LR
            stack1["stack service"]
            stack2["stack service"]
            stackEllipsis["..."]
            stack3["stack service"]
        end
        style sstack fill:none,stroke:none,stroke-width:0px
    end

    subgraph sr[ ]
        direction LR
        svc1["service revision"] 
        svc2["service revision"] 
        svcEllipsis["..."]
        svc3["service revision"]
    end
    style sr fill:none,stroke:none,stroke-width:0px

    app1 -.-> stack1
    app2 -.-> stack2
    app3 -.-> stack3

    stack1 -.-> svc1
    stack2 -.-> svc2
    stack3 -.-> svc3

    APP --> SR

    classDef serviceRevision fill:#f0f0ff,stroke:#9370db,stroke-width:1px
    classDef stackRevision fill:#e6f0e6,stroke:#5c6bc0,stroke-width:2px
    classDef stackService fill:#f5f7ff,stroke:#8c9eff,stroke-width:1px
    classDef appInstance fill:#ffffff,stroke:#424242,stroke-width:1px
    classDef appService fill:#ffffff,stroke:#424242,stroke-width:1px
    classDef ellipsis fill:none,stroke:none

    class svc1,svc2,svc3 serviceRevision
    class SR stackRevision
    class stack1,stack2,stack3 stackService
    class APP appInstance
    class app1,app2,app3 appService
    class stackEllipsis,appEllipsis,svcEllipsis ellipsis
```

Application service is a representation of a [stack service](../stacks/services.md) in an application instance. Or it can be described as a configuration entity created per each service in a stack. It's similar to a stack service inside a stack but exists in the context of an app instance.

When you create a new app, app services created with the default configuration of corresponding stack services. You can further override configuration per specific app instance through app services.

You can also change your stack configuration and then upgrade an app instance's stack with override settings, in this case configurations from stack services will be transferred to app services.

## Configuration

- Each app services can be enabled or disabled
- Service version can be changed
- For stateless services you can change the number of replicas

When an app service's configuration changed, the app instance will be marked as _needs
rebuild_ because configuration may affect the build process.

### Build source

If a service is buildable, app service will have configuration for build source. You can specify a git repository and a reference: branch, tag or commit hash. Build source selected when you create a new app instance but can be also changed in the existing app instance.

### Integrations

If a service provides certain integrations (e.g. backup storage for a database) you can attach [integrations](../integrations/index.md) of the appropriate [types](../integrations/types.md) to an app service.

### Environment variables

Here you can add, remove and override environment variables that will apply to a selected container. Some of the environment variables cannot be removed but can be overridden. Environment variables that cannot be removed can come from the following sources:

- Service manifest. A service may define environment variables in its manifest
- Stack manifest. A stack manifest can override environment variables or add global environment variables that added to all services in the stack
- From linked service, for example, a database link usually adds environment variables with connection credentials
- From [settings](#settings)

Also, Wodby adds the following global variables to every container:

| Variable                 | Description                                                                              |
|--------------------------|------------------------------------------------------------------------------------------|
| `WODBY_APP_NAME`         | Machine name of the application                                                          |
| `WODBY_INSTANCE_NAME`    | Machine name of the application instance                                                 |
| `WODBY_ENVIRONMENT_NAME` | Name of the environment                                                                  |           
| `WODBY_ENVIRONMENT_TYPE` | Type of the environment                                                                  |
| `WODBY_HOSTS`            | List of domains from enabled HTTP routes                                                 |
| `WODBY_PRIMARY_HOST`     | Hostname from the enabled main app service with an HTTP route                            |
| `WODBY_PRIMARY_URL`      | URL (`https` if certificate attached) of the enabled main app service with an HTTP route |

### Resources

Here you can configure resources for a service. You can specify CPU and memory requests and limits. CPU request and limits specified in
_milicores_ where 1000 milicores equal to 1 CPU core. Memory requests and limits specified in
_mebibytes_ where 1024 mebibytes equal to 1 GB.

Please note that resources request affects the deployment of the app service. For example, if your kubernetes cluster does not have enough resources to deploy an app service's pod with a requested amount of CPU or memory, the pod will be in a pending state until the resources become available. If your cluster has horizontal autoscaling enabled, it will scale up number of nodes to meet the demand.

### Replicas

App service replicas is the number of pods (container instances) deployed for the app service. Stateless app services can be easily scaled by increasing the number of replicas to handle increased load and for [high availability](high-availability.md) and redundancy. Replicas can also be increased automatically if [autoscaling](scalability.md) enabled. Some stateful services support scalability with extra replicas, e.g. database server's read replicas.

### Links

Here you can change [links](../services/links.md) between app services. Usually they are set up in a stack but can also be overridden per app instance.

### Volumes

Currently, volumes resize not supported and cannot be changed in an existing app instance. You can only specify volume sizes when you create a new app instance.

### Settings

You can change values of [settings](../services/settings.md)

### Configs

You can view default [configs](../services/configs.md) and override them.

### Tokens

You can add or remove [tokens](tokens.md) that can be used in environment variables.
