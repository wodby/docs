---
description: Deploy all or selected services of an app environment. Covers service ordering, automatic rollback, queueing, first deployments and redeployments.
---

# Application deployments

Deployments can target all services in an app environment or only selected services.

Within a deployment, Wodby orders services using both explicit stack `depends` rules and the current links between app
services. If two linked services are deployed together, the linked target service is deployed first.

Deployments use automatic rollback by default. Rollback is best-effort and applies to the app service release that fails.

Every deployment is associated with a specific stack revision of the app environment.

When a deployment starts, Wodby checks app-service configuration and writes relevant issues to the deployment task as
warnings instead of rejecting the deployment. A full deployment reports issues from all enabled services. A partial
deployment reports issues for its selected services, together with any environment-wide issues. Review these warnings:
the deployment continues, but an affected workload may not operate correctly until its required build source, external
database, integration, linked setting, or other required setting is configured.

Deployments are usually triggered in the following ways:

- automatic first deployment after app creation when services can deploy immediately or build with Wodby CI
- deployment of builds [requested from CI](../cicd/deploy.md)
- automated partial deployments for service-level maintenance
- manual deployment from the UI

## New deployment

A new deployment can be started manually from `Apps > [App] > [Environment] > CI/CD > Deploys > New Deployment`.

In that flow you can:

- choose which services to deploy
- force deployment even when manifests have not changed
- turn deployment scripts on or off for services that provide them (see
  [pre-deployment scripts](#pre-deployment-scripts) for what this switch covers)
- use `Skip rollback on failure` when you want to inspect the failed state instead of restoring the previous deployment;
  it is checked and locked when the environment turns rollback off in its
  [deployment settings](#environment-deployment-settings)
- choose from available successful builds for services with build sources, including eligible older builds
- choose **New build** only when the app service's CI provider and build source support dashboard-triggered builds

If **New build** is unavailable, the build selector explains whether the service needs a linked repository and ref, a
previously recorded GitHub Actions or CircleCI workflow from the selected ref, or whether it uses external-only Custom
CI. A compatible previous successful build remains selectable even when the dashboard cannot start a new one.

When you select **New build** for multiple source owners, Wodby starts the supported builds together and the
deployment waits for exactly the selected owners. Selecting only one source owner does not wait for other buildable
services in the app; a full new-build deployment includes every build-source owner and waits for all of them.

When a selected source owner uses **New build**, selected linked image targets and derivatives that use its output
deploy that same new build, never an older image in the same deployment. A previous successful build selected for
another service is only reused as an image: it does not keep the deployment waiting for another CI run.

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
    environment's stack. Wodby renders the deployment with the current stack revision, configuration, secrets, volumes,
    and linked services. It also does not restore databases or other persistent data.

    An older image can be incompatible with the current database schema, stored data, environment variables, service
    versions, or stack configuration. This risk exists even when the image was built for the current stack revision;
    using an image from another revision adds stack-compatibility risk.

Before starting a build rollback or older-build deployment, the dashboard lists the affected services, build numbers,
and build stack revisions and requires an acknowledgment checkbox. Pre- and post-deployment scripts are turned off by
default for older builds because they can run migrations or other data-changing operations. A migration tool can also
fail on a database that is newer than the older code, which would stop the rollback. In **New Deployment**, you can
explicitly turn a service's scripts back on after reviewing them. The build and deployment detail shortcuts keep those
scripts off. To run them by default for older builds, including from the shortcuts, turn on **Run deployment scripts
for older builds** in the environment's [deployment settings](#environment-deployment-settings).

Deployment history keeps the original build transition visible after the selected build becomes current:

- **Build rollback** means the deployment replaced newer builds entirely with older builds that had been deployed
  successfully before.
- **Includes build rollback** means only some selected services rolled back to previously deployed builds.
- **Older build** means an older selected build had never been deployed before, so it is not labeled as a rollback.
- **Older stack revision** means at least one selected build was created for an earlier stack revision.

Deployment details show the tags per app service together with the previous and selected build numbers, for example
`Build #7 → #5`. These build-selection tags describe the intentional version change; they are separate from automatic
[rollback on rollout failure](#deployment-rollback).

Automatic rollback on rollout failure remains enabled unless you select **Skip rollback on failure** or the environment
turns it off in its [deployment settings](#environment-deployment-settings). That rollback can
restore the previous Kubernetes release after a rollout failure, but it still does not restore application data or
downgrade the stack.

The generic task **Repeat** action remains limited to the latest deployment. To restore an earlier deployment, open its
deployment details and use its **Roll back to this deployment** or **Redeploy** action, which applies the older-build
eligibility checks and confirmation.

### Pre-deployment scripts

CI scripts defined in `.wodby/pre-deployment.yml` run as part of the deployment, before the new build rolls out. Use
them for work the new version needs before it serves traffic, such as database migrations.

- They run when the deployment brings in a new build. A new build always runs them: turning off post-deployment
  scripts, in **New Deployment** or with `--skip-post-deploy`, does not skip them.
- For an older build, including a rollback to an earlier deployment, they follow the service's deployment scripts
  switch, which is off by default for older builds. See
  [Roll back to previous builds and deployments](#roll-back-to-previous-builds-and-deployments).
- They do not run when the deployment keeps the current build, for example a redeploy after a configuration change, an
  automated redeployment, or a stack upgrade that reuses the build.
- They run once per deployment, for the app service that owns the build, and only when that service is included in the
  deployment.
- They run with the new build's image, environment variables and settings. The running version keeps serving until
  they succeed and the rollout finishes.
- If a script fails, the deployment fails before the new version is installed and the previous version keeps serving.
  The deployment's task log shows the script output.
- Deploying the same build again after a failure runs the scripts again, so make them safe to repeat.
- On an app service's first deployment there is no previous version, so the scripts run right after the service is
  installed.
- The service's own [`pre_deploy`](../services/operations.md#pre_deploy) actions, such as a catalog service's
  database migrations, run before the scripts.

!!! warning "Keep migrations compatible with the running version"
    The previous version keeps serving while pre-deployment scripts run and until the rollout finishes. A migration
    that removes or renames a table or column the previous version uses breaks it during that time. Add columns and
    tables before the rollout, and remove or rename them in a later release.

### Post-deployment scripts

CI scripts defined in `.wodby/post-deployment.yml` run in a separate task after the application rollout succeeds. The
deployment and post-deployment task therefore have separate outcomes:

- the deployment is `completed` when the selected app services roll out successfully
- the post-deployment status separately shows whether scripts are pending, running, completed, failed, canceled,
  skipped, not run, or not applicable

A later rollout waits until the deployment and its post-deployment scripts finish. If the rollout fails or is canceled,
the scripts do not run and their status is `not run`.

If a post-deployment script fails, the completed deployment and app environment remain successful. Wodby shows a
post-deployment warning with separate task logs and does not roll back the deployed app services. You can retry the
post-deployment task without redeploying the application while that deployment remains active for the app environment.
After another deployment becomes active, the older deployment's post-deployment task can no longer be retried.

Wodby CLI deployment commands that stream logs or wait for completion follow both tasks. If the rollout succeeds but the
post-deployment task fails, the CLI returns a non-zero exit code with a message that distinguishes the script failure
from deployment failure. `wodby ci deploy` remains asynchronous: it queues the deployment and does not wait for either
task to finish.

### Rollout health checks and failure logs

Applying the Kubernetes resources does not finish a deployment. Wodby waits for the selected workloads to complete
their rollout: the requested replicas must be running the updated workload and pass its readiness checks. Deployments
and DaemonSets must also report the replicas as available. A container can be running while its workload is still
waiting for readiness or a configured minimum-ready interval.

Failure handling depends on the condition:

- **CrashLoopBackOff:** Wodby allows a container about one minute to recover after it first enters this state. This
  applies to both application and init containers. If the container is still in `CrashLoopBackOff` after that, Wodby
  fails the rollout. The first warning therefore does not immediately fail the deployment.
- **Image or container startup errors:** states such as `ErrImagePull`, `ImagePullBackOff`, `InvalidImageName`, and
  `CreateContainerConfigError` fail the rollout when detected, without the crash-loop recovery window.
- **No rollout progress:** a Deployment reporting `ProgressDeadlineExceeded` fails the rollout. Increasing its
  progress deadline does not extend the separate crash-loop recovery window.
- **Pods cannot be scheduled:** the rollout fails if a pod still cannot be scheduled after about seven minutes, or
  three minutes on serverless clusters. Another deployment limit can end the wait sooner.

The one-minute window is not a total deployment timeout: failure diagnostics and automatic rollback can add time. See
[Deployment wait times](../services/deployment.md#deployment-wait-times) for how rollout settings affect other waits.

When a workload fails, Wodby attempts to add pod conditions, container states, warning events, and the previous
container attempt's logs to the task log. Look for **Previous logs** when the current container is waiting in
`CrashLoopBackOff`: the startup error may belong to its previous attempt. The task log may contain only the end of
long output.

### Deployment rollback

When an app service upgrade is applied and its workloads fail health checks, Wodby tries to roll that service release
back to the latest previous successful release. The deployment still fails, but a successful rollback restores that
service to the previous release. The deployment task stays active while rollback runs and waits for the restored
workloads to become ready. The final failure message can therefore appear after the rollback logs, even though the
rollout failure was detected earlier.

Rollback is per app service release. It does not undo other app services that were already deployed successfully during
the same deployment.

Rollback is not always possible. Wodby does not attempt rollback when:

- `Skip rollback on failure` is selected, `--skip-rollback` is used, or the environment turns rollback off in its
  [deployment settings](#environment-deployment-settings)
- the service is being installed for the first time
- the service has no previous successful release
- the failure happens before the Helm upgrade is applied
- the deployment is canceled, interrupted, or times out while waiting for workloads

Wodby also skips rollback when the current and previous release would apply the same Kubernetes resources and there
are no rollback hooks to run. Reapplying that release would not correct the unhealthy workload; the task log explains
why rollback was skipped.

Failures in `.wodby/post-deployment.yml` happen after a successful rollout and never trigger deployment rollback.
Failures in `.wodby/pre-deployment.yml` and in service-manifest `pre_deploy` actions happen before the new version is
installed, so the previous version keeps running and there is nothing to roll back.

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

For non-external services, force deployment restarts the service pods with the selected chart values and image
references, even when those values have not changed.

You do not need force deployment after changing a config file that Wodby mounts into the container. A regular deployment
restarts the service's pods when the file's content changed.

Force deployment does not create a new build or change which image is deployed. For services with build sources, choose the build
you want to deploy in the same way as a regular manual deployment.

Force deployment requires the service to define resolvable workload selectors. If Wodby cannot resolve the workload
selectors for a forced upgrade, the deployment is stopped before the Helm release is changed. External services do not
have Kubernetes workloads to restart.

## Deployment readiness and queueing

`Awaiting` and `Queued` describe different stages of a deployment:

- `Awaiting` means Wodby cannot create the deployment task yet. For example, one or more selected new builds have not
  supplied deployable images, or the target cluster is undergoing an infrastructure upgrade.
- `Queued` means the deployment has everything it needs and its task is waiting for execution capacity or for a
  conflicting deployment or post-deployment operation to finish.

Wodby keeps app-wide deployment operations serialized, but eligible partial deployments can roll out concurrently when
they affect independent resources. If several deployments are requested, each keeps its own service and build selections
and joins that environment's task queue when it becomes ready. Builds can finish in a different order from the requests,
so deployments are queued in readiness order, not necessarily deployment-number order.

### Parallel partial deployments

On Wodby infrastructure version `4.0.0` or newer, an app environment with a working deployment and completed routing
migration can run up to two independent partial deployments at a time. Deployments that share builds, dependencies,
volumes, or certificates wait for one another. Wodby also queues deployments when it cannot establish that they are
independent.

Parallel deployments remain in progress until their shared routing and DNS update finishes. An independent deployment
can succeed even if another fails or is canceled. If the shared routing or DNS update fails, all deployments waiting
for that update fail. Check the task logs before retrying.

First and full deployments, migrations, imports, repository pre- and post-deployment scripts, and deployments of external,
storage, infrastructure, or operator services run one at a time. Environments on older routing infrastructure or with
an unfinished routing migration also run deployments one at a time.

A deployment's repository post-deployment scripts finish before a later rollout starts. If the deployment fails or is
canceled, its scripts do not run.

Starting another deployment does not replace a pending request. Cancel unwanted deployments or their tasks explicitly.

## First deployment

Initial deployment depends on how the app's services are built:

| Build sources | What happens after app creation |
| --- | --- |
| No services need a build | Wodby starts a full deployment immediately. |
| All builds use Wodby CI | Wodby starts the builds and deploys when they are ready. |
| All builds use third-party CI | The app remains `awaiting`. Run your external pipeline and call `wodby ci deploy` to deploy its services with pushed images. |
| Wodby CI and third-party CI | Wodby starts its CI builds and deploys their services without waiting for external pipelines. Run those pipelines to deploy the remaining services. |

During initial setup, build-backed deployments also include all enabled services without build sources while any of
those services has never deployed successfully. After initial setup, a partial deployment includes an unrelated service
without a build source only when it is marked `needs redeploy` and is not already included in another active deployment.
An unhealthy status alone does not add a service to a partial deployment.

Optional build image targets without their own source can use the image produced by their linked owner or their
configured service image when that build does not provide one.

A partial deployment can complete successfully while the app environment remains `awaiting`. The environment becomes `ok`
only after every enabled service that requires a Wodby-managed runtime has a usable deployment. Services omitted from
the first build group can be deployed by their own CI handoff or a later manual deployment.

## Deferred initial deployment

The API can create an app environment with its initial deployment deferred. This lets automation finish configuring the
environment and its services before any application workloads are started. The environment remains `awaiting` until you
explicitly start its first build or deployment.

While the initial deployment is deferred, enabling a service saves the enabled state and marks the app environment as
`needs redeploy`; it does not start an automatic partial deployment. This remains true until the first deployment
completes. Start a deployment that includes the app's required services after configuration is complete.

## Automated redeployments

Some platform operations automatically redeploy only the affected app services. Examples include SSH authorized-key
refreshes and completing an import.

When an affected service uses a build image, Wodby prefers its last successfully deployed build. That known-good image
can be reused after a stack upgrade even though it was built for the previous stack revision. The task log warns when
this happens and shows the selected build and both revision numbers.

An automatic stack upgrade runs repository-defined `.wodby/post-deployment.yml` scripts for a build-source service only
when the upgrade rebuilds that service. If the service needs only a runtime redeployment, Wodby reuses the existing
build and records its post-deployment scripts as `skipped`. This prevents an unchanged build from automatically
repeating migrations or other data-changing jobs. Service-manifest [`pre_deploy`](../services/operations.md#pre_deploy) and
[`post_deploy`](../services/operations.md#post_deploy) actions are separate lifecycle hooks and are not disabled by this repository-script skip. Repository
`.wodby/pre-deployment.yml` scripts follow the same rule: they run only when the upgrade rebuilds the service.

Automatic selection does not search arbitrary build history. Once a newer build is successfully deployed, the previous
build is no longer considered the last known-good image and is not selected automatically across stack revisions. Any
other automatically selected build must be successful, non-voided, and built for the app environment's current stack
revision.

Wodby does not silently replace a missing reusable build with the service's default image. If neither the last
successfully deployed build nor a compatible current-revision build is available, the automated operation stops before
creating the deployment and its task log asks you to run and successfully deploy a new build.

## Routing deployments

On clusters with Wodby infrastructure version `4.0.0` or newer, HTTP routing has a deployment lifecycle separate from
app-service workloads. Wodby can apply these changes without rebuilding images or redeploying app services:

- adding, editing, retargeting, disabling, or deleting a route
- changing app-level or route-specific route settings
- changing HTTP authentication
- issuing or renewing a route certificate

Routing deployments update the complete routing configuration for one app environment.

The app environment shows `Updating routing` while its routing changes have not yet been applied. During a one-time
routing upgrade after the cluster infrastructure upgrade, it shows `Migrating routing`. These states are separate from `needs
rebuild` and `needs redeploy`, which continue to describe app builds and service workloads.

Automatic routing deployments, including deployments after certificate renewal, create background tasks for logs and
failure tracking. You do not need to start an app-service deployment after a successful routing-only change, unless
the change adds or removes a hostname or changes the `Main` domain. Then the app environment is marked `needs redeploy`
so your app receives its new hostnames. See [Domains](endpoints.md#domains).

After a partial workload deployment, Wodby applies routes only for app services that have deployed successfully.
Routes to other services are left out until those services deploy; redirects remain available. The task log identifies
the omitted routes, the app environment returns to `awaiting`, and it remains marked `needs redeploy`. A later workload
deployment adds each route after its service deploys successfully.

Clusters older than infrastructure version `4.0.0` continue to apply route, auth, and certificate changes through the
affected app-service releases. Those apps may still show `needs redeploy` until the cluster infrastructure is upgraded.

## Build deployment

Deployments from CI are triggered with `wodby ci deploy`.

Each build deployment creates a new deployment record associated with the selected build. One build can contain image outputs for multiple app services. CI-triggered deployments can also skip post-deployment scripts for the built services when needed.

A CI build that was not started as part of a dashboard **New build** deploys its own pushed service images without
waiting for unrelated build-source owners. On an app that has not been deployed yet, Wodby also includes the enabled
services without build sources that the first deployment needs. Other build owners remain independent and deploy
when their own builds report back.

Regular app builds can continue while the target cluster is undergoing an infrastructure upgrade. If all required
builds become ready during the upgrade, the deployment remains `awaiting` without a deployment task. Wodby starts it
automatically after the cluster returns to `ok`; you do not need to trigger the deployment again. If the infrastructure
upgrade fails, the deployment continues waiting until the cluster recovers to `ok`.

## Deployment settings

### Environment deployment settings

`Apps > [App] > [Environment] > CI/CD > Deploys > Settings` has a **Deployment behavior** card with defaults for every
deployment of the environment:

- **Run deployment scripts for older builds**, off by default. On, deployments that go back to an older build run its
  pre- and post-deployment scripts, including the **Roll back to this build** and **Roll back to this deployment**
  shortcuts, and **New Deployment** starts with the scripts on. Turn it on only if your scripts are safe to run with
  older code against a newer database.
- **Roll back automatically when a rollout fails**, on by default. Off, a failed rollout stays in place for every
  deployment, including automatic and CI deployments, so you can inspect it. A single deployment cannot turn rollback
  back on while it is off for the environment.

Changing these settings needs permission to configure the environment. They do not require a redeploy.

### App service deployment settings

To change how an app service's pods are replaced during a deployment, open
`Apps > [App] > [Environment] > CI/CD > Deploys > Settings` and select the service in the `App service` selector. See
[Deployment configuration](../services/deployment.md) for the available settings. Saving a change marks the app
environment as needing redeploy.

## Needs redeploy

When app-service configuration changes, the app environment can be marked as `needs redeploy`.

This means configuration has changed, but those changes have not yet been applied to the running deployment.

!!! warning "Auto redeployment"
    Some service-level redeployments happen automatically. Routing-only changes on infrastructure version `4.0.0` or
    newer use a [routing deployment](#routing-deployments) instead and do not restart app-service workloads.
