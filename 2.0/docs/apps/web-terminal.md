# Web Terminal

The web terminal opens an interactive shell session in a running app-service container directly from the dashboard.

It is intended for quick inspection, debugging, and one-off commands without exposing SSH or publishing a port.

No SSH service or public SSH port is required. If you need external shell or file-transfer access from your own terminal,
use [SSH services](../services/types.md#ssh) and, when needed, [published ports](endpoints.md#publishing-ports).

## Where to find it

From `Apps > [App] > [Environment] > Stack > App services > [Service] > Overview`, click `Connect via web terminal`.

## Requirements

To start a session:

- the organization must have an active paid subscription
- you need writable access to the app environment
- the app environment status must be `OK`
- the app service status must be `OK`
- the target service must have at least one workload container and a current pod to connect to
- the cluster must have a current, available Wodby FRPC infrastructure proxy

The dashboard disables `Connect via web terminal` when the organization does not have paid-plan access or when the app
environment or app service is not `OK`. If paid-plan access is missing, hover over the disabled button to see the plan
requirement.

If Wodby cannot find a current pod for the selected workload, the session cannot start.

Web-terminal connections use the cluster's Wodby infrastructure proxy; they do not connect directly to GKE, EKS, or
another provider's Kubernetes API. Clusters created with older infrastructure may need an infrastructure upgrade before
the web terminal is available. This upgrade updates Wodby infrastructure applications and does not move your workloads
or data. Until the proxy is available, Wodby rejects the session instead of falling back to direct provider access.

## Target selection

The web terminal always connects to one container in one current pod of the selected workload.

- If the service has one workload with one container, Wodby opens the session directly
- If the service has multiple workloads, Wodby asks you to choose the workload
- If the selected workload has multiple containers, Wodby asks you to choose the container
- When no explicit selection is required, Wodby uses the [primary workload](../services/workloads.md#primary-workload) and its first container

You cannot choose a specific pod from the dashboard. When a workload has multiple replicas, Wodby connects to one
current pod for that workload.

## Session behavior

- the terminal opens in a separate browser window
- it connects to the live runtime container, not to build containers or completed tasks
- resizing the browser window resizes the terminal session

For build, deploy, cron, and action output, use [Tasks](tasks.md) and [live logs](observability.md#live-logs).
