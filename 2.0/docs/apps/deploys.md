# Application Deployments

Deployments can target all services in an app instance or only selected services.

During the first deployment, Wodby deploys all non-buildable services immediately. Buildable services usually leave the app instance in `awaiting` until a deployment is triggered with build information from a [CI system](../cicd/index.md).

Every deployment is associated with a specific stack revision of the app instance.

Deployments usually triggered in the following ways:

- first deployment after app creation
- deployment of builds [requested from CI](../cicd/deploy.md)
- automated partial deployments, for example after certificate renewal
- manual deployment from the UI

## Build deployment

Deployments from CI are triggered with `wodby ci deploy`.

Each build deployment creates a new deployment record associated with the selected build. One build can contain image outputs for multiple app services. CI-triggered deployments can also skip post-deployment scripts for the built services when needed.

## New deployment

A new deployment can be started manually from `Apps > [App] > Deploys > New Deployment`.

In that flow you can:

- choose which services to deploy
- force deployment even when manifests have not changed
- disable post-deployment scripts for services that provide them
- choose which successful build to deploy for buildable services, as long as the build belongs to the same stack revision as the current app instance

## Needs redeploy

When app-service configuration changes, the app instance can be marked as `needs redeploy`.

This means configuration has changed, but those changes have not yet been applied to the running deployment.

!!! warning "Auto redeployment"
    Some redeployments happen automatically. For example, when a domain certificate is renewed successfully, the related app services may be redeployed automatically.
