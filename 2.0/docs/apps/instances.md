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

Application instance is a single isolated copy of your application that deployed to a [kubernetes cluster](../kubernetes/index.md) and has:

- [Environment](env.md) (like production, staging)
- [Stack](stack.md) with a specific revision 
- [Endpoints](endpoints.md) to configure domains and public ports
- [Builds](builds.md) (if stack contains buildable services) and [deploys](deploys.md)
- [Backups](backups.md) and [imports](imports.md) (if stack contains services that provide such)
- [App Services](services.md) per each service that used to override stack configuration for this specific instance
- Live [logs streaming](observability.md#live-logs) 
- [Cron](cron.md) schedules and jobs 
- [Tasks](tasks.md) history

You can remove or add a new instance from the _"[App] > Instances"_ page.
