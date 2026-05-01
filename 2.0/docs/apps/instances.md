# Instances

``` mermaid
flowchart TD
    subgraph App["<div style='margin-top:10px; white-space: nowrap;'>App</div>"]
        subgraph group[ ]
            Dev["Dev instance"]
            Staging["Staging instance"]
            Prod["Production Instance"]
        end
        style group fill:none,stroke:none,stroke-width:0px          
    end
    
    KubernetesA["Kubernetes Cluster A"]
    KubernetesB["Kubernetes Cluster B"]

    Dev --> KubernetesB
    Staging --> KubernetesB
    Prod --> KubernetesA
```

An app instance is one isolated deployment of your application on a [Kubernetes cluster](../kubernetes/index.md).

Each instance has its own:

- [Environment](env.md), which is a named Env with a fixed type such as `prod`, `staging`, or `dev`
- [Stack](stack.md) revision
- [Endpoints](endpoints.md) to configure domains and public ports
- [Builds](builds.md) and [deploys](deploys.md), when the stack has buildable services
- [Backups](backups.md) and [imports](imports.md), when the stack provides those capabilities
- [App services](services.md) used to override stack configuration for this specific instance
- live [log streaming](observability.md#live-logs)
- [Cron](cron.md) schedules and jobs
- [Tasks](tasks.md) history

All instances of the same app share the same stack, but different instances can run on different clusters and different stack revisions.

App instances do not have a separate project owner. They belong to the app and use the app's ownership and sharing settings.

You add or remove instances from `Apps > [App] > Instances`.

## Related pages

- [Applications overview](index.md)
- [App vs app instance vs app service](app-vs-instance-vs-service.md)
- [Application stack](stack.md)
