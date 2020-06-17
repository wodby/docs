# Stack

## Overview

Stack is a pre-configured infrastructure package for your application. Every stack consist of services, they can be mandatory or optional. Every service has at least one container implementation, e.g. MariaDB or PostgreSQL containers for a database management service.

You can find all stacks offered by Wodby at https://wodby.com/stacks

## Redeployment

Redeployment operation will reload infrastructure of an application's scheme on a server. It is useful if you want to apply updated configuration of multiple services at once. Also, it may be useful for troubleshooting.

During redeployment the entire scheme of an application's infrastructure will be reloaded. However, only services with changes in their configuration will be restarted. For example, if you've updated a container image but did not change image's tag it will not be restarted (for this case we have an API method to force redeployment by image name).