# Stack

Stack is a set of [services](../services/index.md) that you plan to use in your application. To create an application you need to choose a stack, instances of the same application use the same stack but revisions of the stacks they use may differ.

Stack is a versioned entity and can have multiple revisions. Every update made to a stack creates a new revision.

The intended use of a stack is to have a separate stack per each application or sometimes for multiple applications when they are small and alike. This way when you customize a stack you can be sure that all instances (environments) of the same application will get the update.

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

## Updates

When a service in a stack gets a new revision, your stack marked as outdated and can be updated. When you update a stack, the stack in your application will not be automatically updated, you can then upgrade your application stack for each instance individually.

When you create a stack by adding from a catalog this stack marked as one that _has an origin_. Such stack can be additionally _synced with origin_. This may be useful if you want to get some updates from the stack in the catalog (not all stack updates done via services, sometimes there can be an update to a stack itself like addition of a new service or a new stack-wide environment variable).

## Sharing

Stack is a project's entity, it can be shared between multiple projects (with writable or read-only permissions) but must be attached to at least one project.

