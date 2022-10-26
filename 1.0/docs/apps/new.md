# Deploying new application

## Step 1 – choose stack and destination server/cluster

![](../assets/new-app-1.png)

Select one of your [connected servers](../infrastructure/connecting-server.md) or Demo server by Wodby where you want to deploy your applications. 

!!! warning "Demo server"
    All applications deployed to Demo server will be automatically cleaned in 12 hours.

Choose a stack for deployment.

Some [stacks](../stacks/index.md) may provide optional services (e.g. redis as cache storage) that you can either enable or disable in your stack, and multiple implementation for a service (e.g. Nginx or Apache as an HTTP server). You can always enable/disable a service after the deployment from [stack configuration](../stacks/config.md) page.

## Step 2 – configure your application instance

![](../assets/new-app-2.png)

Enter the name of your application and select the [instance type](instances.md) (Dev by default). Your application hostname will be automatically generated based on the name, you can optionally adjust it. You can change all these settings later after initial deployment. We will generate [technical *.wodby.cloud domains](domains.md#technical-wodby-domain-name) based on this.  

## Step 3 – stack configuration (optional)

Some stacks like Drupal and WordPress provide additional configuration on step 3 such as a code [deployment workflow](deploy.md) and import.
