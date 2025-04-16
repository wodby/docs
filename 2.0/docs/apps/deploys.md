# Application Deployments

Deployments are selective and can be performed for specific services. During the first deployment all services deployed except buildable services. For buildable services the app instance's status set to `awaiting` until deployment with the build information triggered from [CI system](../cicd/index.md).

A deployment always associated with a specific revision of app instance's stack's revision.

Deployments usually triggered in the following ways:

- First deployment after app instance creation
- Deployment of builds [requested from CI](../cicd/deploy.md)
- Automated partial deployments (e.g. TSL certificates renewed)
- Manual deployment from UI

## Build deployment

Deployments from CI system can be triggered with `wodby ci deploy` command. For build deployment request a new deployment created associated with the build. Associated build can have multiple app service builds associated. Deployment from CI can optionally disable run of post-deployment scripts for the built services.

## New deployment

A new application deployment can be manually run from _Apps > [App] > Deploys > New Deployment_ page. Services to include to the deployment can optionally be run with the force flag, for such deployments a random hash will be added to the Kubernetes annotations to force actual resources deployment even if there are no changes in manifests. Post-deployments are enabled by default for services that provide them but can be disabled. For buildable service last successful build selected by default but can be chosen to older builds as long as the build's associated stack revision and the current app instance's stack revision are the same.

## Needs redeploy

When app service's configuration changed app instance's will be marked as `needs redeploy`. It is to indicate that although changes has been done to the app services they are not yet applied.

!!! warning "Auto redeployment"
    
    Please note that app instance can sometimes be redeployed automatically, for example when domains' certificates renewed the associated app services will be redeployed automatically when renewal succeeded. 
