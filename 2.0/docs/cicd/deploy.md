# Continuous Deployments

This page covers deployments triggered by CI. For more information about deployments in general see [app deploys](../apps/deploys.md).

Use `wodby ci deploy [SERVICE]...` to deploy previously released images. If you do not specify services, Wodby deploys all released services from the current build.

Each CI deployment is associated with the Wodby build created during `wodby ci init`. You can review the deployment
history, including failed deployments, from `Apps > [App] > [Instance] > CI/CD > Deploys`.

CI-triggered deployments use the same [rollback behavior](../apps/deploys.md#deployment-rollback) as manual deployments.

## Post-deployment scripts

If the build contains `.wodby/post-deployment.yml`, Wodby runs those jobs after the deployment completes. Pass `--skip-post-deploy` to `wodby ci deploy` when you want to skip them for a specific deployment.
