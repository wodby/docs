# Maintenance mode

App instance maintenance mode temporarily replaces enabled public HTTP and HTTPS routes with a Wodby maintenance
response. Use it when visitors should see a consistent maintenance page while you continue running deployments,
migrations, or other work inside the application.

Maintenance mode changes routing only. It does not stop application workloads or change the app instance lifecycle
status.

## Enable maintenance mode

1. Open `Apps > [App] > [Instance] > Settings > Maintenance`.
2. Select `Enable maintenance mode`.
3. Review the affected traffic and confirm.
4. Follow the routing task if the dashboard opens it.

The maintenance status moves from `Off` to `Enabling` while Wodby applies the routing change, then to `Active` after
the public edge confirms it. The app instance keeps its normal lifecycle status, such as running, deploying, awaiting,
or errored. Instance headers and lists show a separate maintenance badge.

Enabling maintenance mode requires a non-infrastructure app instance with ready platform-managed routing. You can
change maintenance mode while the instance is running, awaiting a deployment, errored, or deploying. The cluster must
support the direct-response routing capability used for the fixed page. If the capability is unavailable, the
dashboard leaves maintenance mode off and explains the requirement.

## Traffic behavior

While maintenance mode is active, every enabled public Wodby HTTP or HTTPS route for the app instance returns the same
fixed page with:

- HTTP status `503 Service Unavailable`
- `Retry-After: 300`, asking clients to retry after five minutes
- `Cache-Control: no-store`
- search-engine no-index headers

The page is served at the public edge and does not depend on an application container. It is fixed and cannot be
customized. Existing hostname and path matching, TLS certificates, HTTP-to-HTTPS redirects, and HTTP basic
authentication remain in place.

Maintenance mode also covers public redirect routes. A route configured to redirect to another destination returns
the maintenance response until maintenance mode is disabled.

The following traffic is not replaced:

- routes marked private
- routes suppressed because [App Access](access.md) publishes them through a protected or private provider path
- published TCP or UDP ports

With Selected endpoints App Access, any ordinary public routes outside the selected scope still receive the
maintenance response. Provider-managed protected or private endpoints continue using their normal provider path.

## Workloads, tasks, and billing

Application workloads remain running. Scheduled jobs, builds, deploys, backups, and other application operations
continue according to their normal rules. Maintenance mode does not reduce app-service plan usage or infrastructure
costs.

A workload deployment and a maintenance request can overlap. When necessary, Wodby waits for the workload deployment
before applying the pending routing change. Follow the routing task to see its progress or failure details.

You cannot pause an app instance while maintenance mode is requested or active. Disable maintenance mode and wait for
its status to return to `Off`, then use `Settings > Pause & Resume`. See
[Pausing and resuming an instance](instances.md#pausing-and-resuming-an-instance).

## Disable or reverse maintenance mode

Open `Settings > Maintenance` and select `Disable maintenance mode`. The status changes to `Disabling` while Wodby
restores application backends to the public routes, then returns to `Off` after the public edge confirms the change.
Visitors may continue to receive the maintenance response during this transition.

You can reverse a pending request. For example, select `Disable maintenance mode` while the status is `Enabling`, or
select `Enable maintenance mode` while it is `Disabling`. Wodby finishes or supersedes the in-progress routing change
and converges on the latest requested state.

If a routing task fails, the requested and active states can differ. The dashboard continues to show `Enabling` or
`Disabling` instead of reporting a completed change. Review the task logs, correct the routing or cluster problem, and
retry the failed routing task.

## Maintenance mode compared with pausing

| Behavior | Maintenance mode | Paused instance |
| --- | --- | --- |
| Public HTTP and HTTPS routes | Fixed `503` maintenance response | Do not respond |
| Application workloads | Continue running | Stop |
| Scheduled jobs | Continue normally | Stop and skip runs that become due |
| Builds and deploys | Continue normally | Cannot start |
| Persistent data | Remains provisioned | Remains provisioned |
| App-service plan usage | Unchanged | Stops after pause completes |
| TCP and UDP ports | Unchanged | Do not respond with the stopped workloads |

Use maintenance mode when the application must keep running behind a temporary public response. Use pause when the
instance is not needed and its workloads should release compute and memory.

## Related pages

- [App instances](instances.md)
- [Endpoints](endpoints.md)
- [App access](access.md)
- [Deploys and routing deployments](deploys.md#routing-deployments)
