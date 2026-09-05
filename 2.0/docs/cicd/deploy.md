# Continuous Deployments

This page covers deployments triggered by CI. For more information about deployments in general see [app deploys](../apps/deploys.md).

Use `wodby ci deploy [SERVICE]...` to deploy previously released images. If you do not specify services, Wodby deploys all released services from the current build.

Each CI deployment is associated with the Wodby build created during `wodby ci init`. You can review the deployment
history, including failed deployments, from `Apps > [App] > [Environment] > CI/CD > Deploys`.

CI-triggered deployments use the same [rollback behavior](../apps/deploys.md#deployment-rollback) as manual deployments.

## Post-deployment scripts

If the build contains `.wodby/post-deployment.yml`, Wodby runs those jobs in a separate task after the application
rollout completes. Pass `--skip-post-deploy` to `wodby ci deploy` when you want to skip them for a specific deployment.

When the deployment becomes ready, Wodby places an eligible post-deployment task immediately after its rollout in the
app environment's queue. A later rollout cannot run between the rollout and its scripts. If the rollout fails or is
canceled, the scripts do not run and the post-deployment status is `not run`.

A post-deployment failure does not change the successful deployment or app status and does not trigger rollback.
Deployment details show a separate post-deployment warning and task log. You can retry only the failed
post-deployment task without redeploying the application.

`wodby ci deploy` records the released build as deployable and returns without waiting for the rollout or
post-deployment task. The deployment can remain `Awaiting` while other selected builds finish or the cluster completes
infrastructure maintenance. When all inputs are ready, its normal deployment task becomes `Queued` until execution
capacity is available. Eligible independent partial deployments can roll out concurrently; conflicting deployments and
deployments with post-deployment scripts remain ordered. See
[Deployment readiness and queueing](../apps/deploys.md#deployment-readiness-and-queueing) and
[parallel partial deployments](../apps/deploys.md#parallel-partial-deployments).

Operational CLI commands that stream deployment logs or explicitly wait for a deployment follow both tasks and return
a non-zero exit code when the post-deployment task fails. The error identifies that the rollout completed successfully
and the failure came from post-deployment scripts.
