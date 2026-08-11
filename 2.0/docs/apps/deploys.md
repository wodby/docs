# Application Deployments

Deployments can target all services in an app instance or only selected services.

Within a deployment, Wodby orders services using both explicit stack `depends` rules and the current links between app
services. If two linked services are deployed together, the linked target service is deployed first.

Deployments use automatic rollback by default. Rollback is best-effort and applies to the app service release that fails.

During the first deployment, Wodby deploys services without a build source immediately. Services with build sources usually leave the app instance in `awaiting` until a deployment is triggered with build information from a [CI system](../cicd/index.md). Optional build image targets without their own build source can still deploy with their configured service image when the build does not provide a custom image for them.

Every deployment is associated with a specific stack revision of the app instance.

Deployments require complete configuration for all enabled app services in the app instance. Wodby blocks deployment
when a service is missing a required build source, external database, integration, linked setting, or required setting.

Deployments are usually triggered in the following ways:

- first deployment after app creation
- deployment of builds [requested from CI](../cicd/deploy.md)
- automated partial deployments for service-level maintenance
- manual deployment from the UI

## Deferred initial deployment

The API can create an app instance with its initial deployment deferred. This lets automation finish configuring the
instance and its services before any application workloads are started. The instance remains `awaiting` until you
explicitly start its first build or deployment.

While the initial deployment is deferred, enabling a service saves the enabled state and marks the app instance as
`needs redeploy`; it does not start an automatic partial deployment. This remains true until a deployment establishes
the app's runtime and active route backends. Start a deployment that includes the app's required services after
configuration is complete.

## Automated redeployments

Some platform operations automatically redeploy only the affected app services. Examples include SSH authorized-key
refreshes and completing an import.

When an affected service uses a build image, Wodby prefers its last successfully deployed build. That known-good image
can be reused after a stack upgrade even though it was built for the previous stack revision. The task log warns when
this happens and shows the selected build and both revision numbers.

Automatic selection does not search arbitrary build history. Once a newer build is successfully deployed, the previous
build is no longer considered the last known-good image and is not selected automatically across stack revisions. Any
other automatically selected build must be successful, non-voided, and built for the app instance's current stack
revision.

Wodby does not silently replace a missing reusable build with the service's default image. If neither the last
successfully deployed build nor a compatible current-revision build is available, the automated operation stops before
creating the deployment and its task log asks you to run and successfully deploy a new build. Selection logs use build
numbers, service names, and stack revision numbers without exposing internal entity IDs.

## Routing deployments

On clusters with Wodby infrastructure version `4.0.0` or newer, HTTP routing has a deployment lifecycle separate from
app-service workloads. Wodby can apply these changes without rebuilding images or redeploying app services:

- adding, editing, retargeting, disabling, or deleting a route
- changing app-level or route-specific route settings
- changing HTTP authentication
- issuing or renewing a route certificate

Routing deployments update the complete routing configuration for one app instance. Repeated changes made while an
update is running are combined and followed by another routing update when necessary.

The app instance shows `Updating routing` while its desired routing configuration has not yet been applied. During the
one-time upgrade from service-owned routing, it shows `Migrating routing`. These states are separate from `needs
rebuild` and `needs redeploy`, which continue to describe app builds and service workloads.

Automatic routing deployments, including deployments after certificate renewal, create background tasks for logs and
failure tracking. You do not need to start an app-service deployment after a successful routing-only change.

After a partial workload deployment, Wodby applies routing for app services that currently have a successful deployed
runtime. Routes to services that have not deployed successfully are omitted instead of being applied to missing
Kubernetes Services; redirects remain available because they do not require a service backend. The task log identifies
omitted backends, the app instance returns to `awaiting`, and it remains marked `needs redeploy`. A later workload
deployment reevaluates every service and adds each route after its backend becomes available.

Clusters older than infrastructure version `4.0.0` continue to apply route, auth, and certificate changes through the
affected app-service releases. Those apps may still show `needs redeploy` until the cluster infrastructure is upgraded.

## Build deployment

Deployments from CI are triggered with `wodby ci deploy`.

Each build deployment creates a new deployment record associated with the selected build. One build can contain image outputs for multiple app services. CI-triggered deployments can also skip post-deployment scripts for the built services when needed.

Regular app builds can continue while the target cluster is undergoing an infrastructure upgrade. If all required
builds become ready during the upgrade, the deployment remains `awaiting` without a deployment task. Wodby starts it
automatically after the cluster returns to `ok`; you do not need to trigger the deployment again. If the infrastructure
upgrade fails, the deployment continues waiting until the cluster recovers to `ok`.

## New deployment

A new deployment can be started manually from `Apps > [App] > [Instance] > CI/CD > Deploys > New Deployment`.

In that flow you can:

- choose which services to deploy
- force deployment even when manifests have not changed
- disable post-deployment scripts for services that provide them
- use `Skip rollback on failure` when you want to inspect the failed state instead of restoring the previous deployment
- choose from available successful builds for services with build sources, including eligible older builds
- choose **New build** only when the app service's CI provider and build source support dashboard-triggered builds

If **New build** is unavailable, the build selector explains whether the service needs a linked repository, branch or
tag, GitHub workflow, or previous CircleCI workflow, or whether it uses external-only Custom CI. A compatible previous
successful build remains selectable even when the dashboard cannot start a new one.

If you deploy only a subset of services, Wodby applies that ordering only inside the selected set. Repository
post-deployment scripts run only when the app service that owns the corresponding build is included in the selected
deployment. Reusing that build for another selected service does not make the build owner's scripts applicable.

### Roll back to previous builds and deployments

You can manually move app services back to versions produced by earlier builds in three places:

- select an older build for one or more services in **New Deployment**
- open a build that was deployed before and is older than the currently deployed build, then select **Roll back to this
  build**; an older build that was never deployed instead uses **Deploy this older build**
- open an earlier deployment and select **Roll back to this deployment** when it restores older, previously deployed
  builds; otherwise the action remains **Redeploy**

The build selector lists only eligible images. It marks an image that is in use as **Currently deployed** and shows an
**Older stack revision** warning on selectable images built for an earlier stack revision. A completed, non-voided
image from the current stack revision can be selected even if it has never been deployed before. An image from an older
stack revision is selectable only when that exact app-service image completed a deployment previously. Missing, voided,
incomplete, and ineligible cross-revision images remain visible in build history but are omitted from the selector. The
selector groups eligible previous choices under **Older builds**.

!!! warning "A build rollback uses the current stack"
    Rolling back to a previous build—or deploying an older build that was never deployed—does not downgrade the app
    instance's stack. Wodby renders the deployment with the current stack revision, configuration, secrets, volumes,
    and linked services. It also does not restore databases or other persistent data.

    An older image can be incompatible with the current database schema, stored data, environment variables, service
    versions, or stack configuration. This risk exists even when the image was built for the current stack revision;
    using an image from another revision adds stack-compatibility risk.

Before starting a build rollback or older-build deployment, the dashboard lists the affected services, build numbers,
and build stack revisions and requires an acknowledgment checkbox. Post-deployment scripts are turned off by default for
older builds because they can run migrations or other data-changing operations. In **New Deployment**, you can
explicitly turn a service's scripts back on after reviewing them. The build and deployment detail shortcuts keep those
scripts off; use **New Deployment** if you intentionally need to run them.

Deployment history keeps the original build transition visible after the selected build becomes current:

- **Build rollback** means the deployment replaced newer builds entirely with older builds that had been deployed
  successfully before.
- **Includes build rollback** means only some selected services rolled back to previously deployed builds.
- **Older build** means an older selected build had never been deployed before, so it is not labeled as a rollback.
- **Older stack revision** means at least one selected build was created for an earlier stack revision.

Deployment details show the tags per app service together with the previous and selected build numbers, for example
`Build #7 → #5`. These build-selection tags describe the intentional version change; they are separate from automatic
[rollback on rollout failure](#deployment-rollback).

Automatic rollback on rollout failure remains enabled unless you select **Skip rollback on failure**. That rollback can
restore the previous Kubernetes release after a rollout failure, but it still does not restore application data or
downgrade the stack.

The generic task **Repeat** action remains limited to the latest deployment. To restore an earlier deployment, open its
deployment details and use its **Roll back to this deployment** or **Redeploy** action, which applies the older-build
eligibility checks and confirmation.

### Post-deployment scripts

CI scripts defined in `.wodby/post-deployment.yml` run in a separate task after the application rollout succeeds. The
deployment and post-deployment task therefore have separate outcomes:

- the deployment is `completed` when the selected app services roll out successfully
- the post-deployment status separately shows whether scripts are pending, running, completed, failed, canceled,
  skipped, or not applicable

If a post-deployment script fails, the completed deployment and app instance remain successful. Wodby shows a
post-deployment warning with separate task logs and does not roll back the deployed app services. You can retry the
post-deployment task without redeploying the application while that deployment remains active for the app instance.
After another deployment becomes active, the older deployment's post-deployment task can no longer be retried.

Wodby CLI deployment commands that stream logs or wait for completion follow both tasks. If the rollout succeeds but the
post-deployment task fails, the CLI returns a non-zero exit code with a message that distinguishes the script failure
from deployment failure. `wodby ci deploy` remains asynchronous: it queues the deployment and does not wait for either
task to finish.

### Deployment rollback

When an app service upgrade is applied and its workloads fail health checks, Wodby tries to roll that service release
back to the latest previous successful release. The deployment still fails, but a successful rollback restores that
service to the previous release.

Rollback is per app service release. It does not undo other app services that were already deployed successfully during
the same deployment.

Rollback is not always possible. Wodby does not attempt rollback when:

- `Skip rollback on failure` is selected or `--skip-rollback` is used
- the service is being installed for the first time
- the service has no previous successful release
- the failure happens before the Helm upgrade is applied
- the deployment is canceled, interrupted, or times out while waiting for workloads

Failures in `.wodby/post-deployment.yml` happen after a successful rollout and never trigger deployment rollback.

If rollback is not attempted, the failed release state remains in the cluster. If rollback is attempted but fails, the
deployment remains failed and the task logs include the rollback error.

Deployment history and deployment details show rollback status when Wodby rolled back successfully or when rollback
failed. Deployments without a rollback do not show a rollback status.

Failed deployment notifications include whether Wodby rolled back, did not roll back, or attempted rollback and failed.

### App service status after deployment

An app service's status reflects the outcome of its own rollout, not just the overall deployment:

- A successful rollout sets the app service to `ok`, or `disabled` when the service is disabled.
- If an earlier check or dependency failure prevents the service rollout from starting, Wodby keeps the service's
  previous status. Its deployment is canceled and the service remains marked for redeploy.
- If the service rollout starts and then fails or is canceled, the app service becomes `errored`.
- If that failed rollout is successfully rolled back, Wodby restores the service's previous healthy `ok` or `disabled`
  status. The deployment still fails and the service remains marked for redeploy.

A successful build does not change an app service's deployment status. After a rollout error, deploy the service again
to clear the error, unless an automatic rollback already restored its previous healthy status.

### Force deployment

Use force deployment when you need Wodby to redeploy a selected app service even though the rendered Kubernetes
manifests have not changed.

For non-external services, Wodby runs the normal Helm upgrade and then updates the pod template of each resolved
Deployment, StatefulSet, or DaemonSet with an internal redeploy annotation. Kubernetes treats the pod-template update as
a new rollout, so the service pods are restarted with the same chart values and image references.

Force deployment does not create a new build or change which image is deployed. For services with build sources, choose the build
you want to deploy in the same way as a regular manual deployment.

Force deployment requires the service to define resolvable workload selectors. If Wodby cannot resolve the workload
selectors for a forced upgrade, the deployment is stopped before the Helm release is changed. External services do not
have Kubernetes workloads to restart.

## Needs redeploy

When app-service configuration changes, the app instance can be marked as `needs redeploy`.

This means configuration has changed, but those changes have not yet been applied to the running deployment.

!!! warning "Auto redeployment"
    Some service-level redeployments happen automatically. Routing-only changes on infrastructure version `4.0.0` or
    newer use a [routing deployment](#routing-deployments) instead and do not restart app-service workloads.
