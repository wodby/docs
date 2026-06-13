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
- [Endpoints](endpoints.md) to configure HTTP routes and published ports
- [Builds](builds.md) and [deploys](deploys.md), when the stack has services with build configuration
- [Backups](backups.md) and [imports](imports.md), when the stack provides those capabilities
- [App services](services.md) used to override stack configuration for this specific instance
- [Metrics](observability.md#metrics), when cluster monitoring is enabled
- live [log streaming](observability.md#live-logs)
- [Cron](cron.md) schedules and jobs
- [Tasks](tasks.md) history

All instances of the same app share the same stack, but different instances can run on different clusters and different stack revisions.

App instances do not have a separate project owner. They belong to the app and use the app's ownership and sharing settings.

The instance machine name is permanent and must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names). The generated namespace, `<app-name>-<instance-name>`, must be 63 characters or shorter.

You add or remove instances from `Apps > [App] > Instances`.

## Errored instances

An app instance can move to `errored` when Wodby cannot finish creating it or cannot finish deletion cleanup.

Errored instances remain visible so you can inspect task logs and delete the instance. Operations that would create new
runtime work or change deployable configuration are blocked, including new builds and deployments, stack upgrades,
service configuration changes, route and auth changes, app-scoped backups, cron jobs, shell sessions, live logs, pod
queries, and container-backed database changes. Automatic app-scoped schedules such as backups, cron jobs, and
certificate renewals skip errored instances.

Review the failed task to find the cause. After fixing the underlying problem, delete the errored instance and create a
new one.

## Related pages

- [Applications overview](index.md)
- [App vs app instance vs app service](app-vs-instance-vs-service.md)
- [Application stack](stack.md)
