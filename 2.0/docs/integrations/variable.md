# Variable integration

Variable integration is the way to add environment variables to your applications. It's the same effect as if you would simply add environment variables directly to your app but this way you can group environment variables per third-party service (for example _license_ and _app name_ environment variables needed for NewRelic integration). Also, this allows to unify integration across your applications and update them simultaneously if required. You can add variable integrations to you stack, so all app instances created from this stack will have the same set of environment variables. 

## Variable provider

We try to offer a wide range of variable providers but if you can't find the one you can always create your own variable provider and assign names of environment variables that will be added.  You can create your own variable providers from the _"Providers > New variable provider"_ page. 
