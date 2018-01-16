# Deploying New Application with Wodby

Deployment of the new applications consist of 2 simple steps:

### Step 1: Choose Server and Stack

![](_images/new-app-1.png)

Select one of the [**connected servers**](../servers/README.md) where you want to deploy your app. 
 
Choose a [**stack**](../stacks/README.md) for deployment. 

Some stacks may provide optional services such as optional cache storage and multiple implementation for service, e.g. Nginx or Apache for HTTP server. You'll be able to change it after deployment (see [stack configuration](/stacks/configuration.md)). 
 
### Step 2: Configuration application instance

![](_images/new-app-2.png)

Enter the name of your application and select [instance type](instances.md) (Dev by default). The URL for your application will be automatically generated based on the name, you can optionally adjust it. You can change all these settings later after initial deployment.

### Optional Step 3: stack configuration

Some stacks like Drupal and WordPress provide additional configuration on step 3 such as code deployment workflow and import.
