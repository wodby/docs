# Application Environment

## Overview

``` mermaid
flowchart TD
    subgraph App["<div style='margin-top:10px; white-space: nowrap;'>App</div>"]
        subgraph group[ ]
            Dev["Dev instance"]
            Feature["Feature instance"]
            Prod["Production Instance"]
        end
        style group fill:none,stroke:none,stroke-width:0px          
    end
    
    EnvA["Production (type: prod)"]
    EnvB["Dev (type: dev)"]

    Prod --> EnvA
    Dev --> EnvB
    Feature --> EnvB
```

Environment on Wodby is essentially a tag to define a context for application instance (and also [databases](../databases/index.md) and [kubernetes clusters](../kubernetes/index.md)) to separate production, development, testing and staging. This context can later be used when configuring your application (e.g. add environment variable but only for
production instances).

Environments can be created by a user in addition to default environments.

Environment has a type, at least one environment must per type.

## Type

The following environment types supported:

- `dev`
- `prod`
- `staging`
- `testing`
- `feature`
