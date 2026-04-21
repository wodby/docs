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

An Environment (Env) is an organization-level object that defines deployment context.

App instances, [databases](../databases/index.md), and some other resources are assigned to an Env. The Env itself is not the deployment. It is the label and matching context around that deployment.

Each Env has:

- a name and title
- a type chosen from a fixed enum
- organization-level reuse across apps and other resources

Multiple Envs can share the same type. For example, `Production EU` and `Production US` can both use the `prod` type.

This type matters because stack- and service-level configuration can target an environment type, not only a single named Env.

Organizations start with default Envs for the standard types, and you can create additional named Envs as needed.

## Environment types

The current environment type enum is:

- `prod`
- `staging`
- `test`
- `dev`
- `feature`
