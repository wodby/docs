# Stack

A stack is the blueprint for an application.

It defines which [services](../services/index.md) the app uses and the default configuration for those services. To create an app, you choose a stack first.

All app instances of the same app share the same stack, but they can run different published stack revisions.

Stacks are versioned. Changes made in the dashboard are saved to an unpublished draft revision first. Publishing the draft creates a new stack revision. Discarding the draft removes the unpublished changes.

The usual model is one stack per application. In some cases, multiple small similar apps may share a stack, but separate stacks are easier to evolve safely over time.

Public Wodby stacks are listed in [`wodby/stacks`](https://github.com/wodby/stacks), with links to their source
repositories. To create a new stack in Git, start from the [`wodby/stack`](https://github.com/wodby/stack)
boilerplate.

## Create

You can create stacks from the dashboard catalog, from scratch in the dashboard, by duplicating an existing stack, from
Git, from a local manifest, or from a Helm scaffold.

After creation, all paths produce regular versioned stacks. You can adjust their [configuration](configuration.md), add
or remove stack services, publish changes as revisions, and create apps from any available published revision.

See [Create a stack](create.md).

## Model

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

When a service used by the stack gets a new revision, or when stack-level configuration changes, the stack can become
outdated. Configuration edits create or update an unpublished draft first. Stack service revision updates, Git updates,
sync with origin, and automatic stack updates create a new stack revision directly after the update task succeeds.

Stacks can update stack service revisions to use the latest available service revisions without changing which services
the stack contains. Git-backed stacks can also update from Git, either manually or through Git auto-update when a
supported push event matches the stack source. Catalog-derived stacks can sync with their origin to pull in catalog-side
manifest changes.

Publishing the draft creates a new stack revision. Updating a stack does not automatically update all app instances
using it unless the stack was updated automatically and auto-upgrade is enabled for those app instances. Each app
instance can still be upgraded to the latest published stack revision separately.

See [Stack updates](updates.md) for the stack update workflows and [Application stack](../apps/stack.md#upgrade) for
the app instance upgrade settings.

## Sharing

A stack can be project-owned or organization-owned. Sharing makes the stack visible and usable in additional projects. A `Modify/Delete` share marks the project-stack link as write-capable where supported, without changing the owner.

See [Sharing](../sharing.md) and [Access control](../access-control.md) for the full ownership and permission model.
