# Application Deployments

Deployments can target all services in an app instance or only selected services.

Within a deployment, Wodby orders services using both explicit stack `depends` rules and the current links between app
services. If two linked services are deployed together, the linked target service is deployed first.

Deployments are transactional by default. If one of the app service deployments fails, Wodby rolls back the entire deployment.

During the first deployment, Wodby deploys services without a build source immediately. Services with build sources usually leave the app instance in `awaiting` until a deployment is triggered with build information from a [CI system](../cicd/index.md). Optional build image targets without their own build source can still deploy with their configured service image when the build does not provide a custom image for them.

Every deployment is associated with a specific stack revision of the app instance.

Deployments require complete configuration for all enabled app services in the app instance. Wodby blocks deployment
when a service is missing a required build source, external database, integration, linked setting, or required setting.

Deployments are usually triggered in the following ways:

- first deployment after app creation
- deployment of builds [requested from CI](../cicd/deploy.md)
- automated partial deployments, for example after certificate renewal
- manual deployment from the UI

## Build deployment

Deployments from CI are triggered with `wodby ci deploy`.

Each build deployment creates a new deployment record associated with the selected build. One build can contain image outputs for multiple app services. CI-triggered deployments can also skip post-deployment scripts for the built services when needed.

## New deployment

A new deployment can be started manually from `Apps > [App] > [Instance] > CI/CD > Deploys > New Deployment`.

In that flow you can:

- choose which services to deploy
- force deployment even when manifests have not changed
- disable post-deployment scripts for services that provide them
- use `Skip rollback on failure` when you want to inspect the failed state instead of restoring the previous deployment
- choose which successful build to deploy for services with build sources, as long as the build belongs to the same stack revision as the current app instance

If you deploy only a subset of services, Wodby applies that ordering only inside the selected set.

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
    Some redeployments happen automatically. For example, when a route certificate is renewed successfully, the related app services may be redeployed automatically.
