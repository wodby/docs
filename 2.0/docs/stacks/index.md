# Stack

Stack is a set of [services](../services/index.md) that you plan to use in your application. To create an application you need to choose a stack, instances of the same application use the same stack but revisions of the stacks they use may differ.

Stack is a versioned entity and can have multiple revisions. Every update made to a stack creates a new revision.

## Configuration

The intended use of a stack is to have a separate stack per each application or sometimes for multiple applications when they are small and alike. This way when you customize a stack you can be sure that all instances (environments) of the same application will get the update.

Unlike Wodby 1.0 there's no differences between managed and custom stacks. All stacks are custom and supposed to be changed to your needs. And at the same time all stacks get updates from the included managed services.

### Environment Variables

You can add stack-wide environment variables from "[Stack] > Configure > Env vars" page. Such environment variables will be added to all app services' kubernetes resources during deployment in app instances that use this stack revision. 

An environment variable can be optionally marked as secret, when "Secret" selected the environment variable value will be stored in a kubernetes secret and won't be shown in Wodby dashboard. 

You can optionally limit a variable to a certain environment type, when set env var will be added only to app instances that use the selected environment type.

### Annotations

You can add stack-wide annotations from "[Stack] > Configure > Annotations" page. Such annotations will be added to all app services' kubernetes resources during deployment in app instances that use this stack revision.

You can optionally limit an annotation to a certain environment type, when set annotations will be added only to app instances that use the selected environment type.

### Tokens

You can add stack-wide tokens from "[Stack] > Configure > Tokens" page. Such tokens will be added to all app services in app instances that use this stack revision. 

Tokens can either have a plain value or a regular expression that will be used to generate a random secret value when an app services created/updated. You can use tokens in environment variables' value. 

You can optionally limit a token to a certain environment type, when set tokens will be added only to app instances that use the selected environment type.

### Services

A stack always includes a specific revision of a service. When a new service revision issued corresponding stacks can be updated to switch to the latest revision of a service. 

Each service in a stack can be configured under "[Stack] > Configure > Stack services > [Service]". A service can be enabled or disabled, set as mandatory or optional. When set mandatory it cannot be excluded during new app creation.

Only one service can be set as main, in this case, if a service has http endpoints, the app instance's main technical domain will target the main endpoint of the main app service.

#### Replicas

You can change number of replicas per service, not available for external services.

#### Integrations

If a service provides integrations in its manifest, you can link a specific integration from your project that satisfies requirements of a service integration. Example: OpenSMTPD service allows `smtp` typed integrations to be connected to use as relay, a user has _Brevo_ integration in her organization and selects it under "[Stack] > Configure > Stack services > OpenSMTPD > Integrations", then creates a new app with this Stack, the app will already have _Brevo_ integration connected and will use it to send emails from OpenSMTPD. 

Additionally, to all non-external services you can add [Variable](../integrations/variable.md) integrations.

#### Environment Variables

You can add service-specific environment variables from _"[Stack] > Configure > Stack services > [Service] > Env vars"_ page. Such environment variables will be added to the corresponding app service's kubernetes resources during deployment in app instances that use this stack revision.

An environment variable can be optionally marked as secret, when "Secret" selected the environment variable value will be stored in a kubernetes secret and won't be shown in Wodby dashboard.

You can optionally limit a variable to a certain environment type, when set env var will be added only to app instances that use the selected environment type.

#### Resources

For non-external services you can set up resources requests and limits from _"[Stack] > Configure > Stack services > [Service] > Resources"_ page. Resources requests and limits correspond to [kubernetes resources request and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-limits-are-run). 

##### Request

You may set up request for CPU and memory. Requests help your cluster to schedule and distribute workloads across the nodes. When resources request specified your deployments may fail if there are not enough resources on the cluster. CPU requests are mandatory for scalability. 

##### Limit

You may set up limits for CPU and memory. Resources limits are useful to limit burstable workloads and their effect on other resources on the same cluster.  

#### Options

Options represent different versions or variant of a service. Some stacks may limit which options are supported (enabled) to match with compatibility requirements or to exclude end of life (EOL) versions. You can change the default option and enabled options for a service in your stack from _"[Stack] > Configure > Stack services > [Service] > Options"_ page.

#### Links

A service may provide a _link_, it's a way to represent integration of a service with another service. The simplest example would be Nginx's service link to upstream/backend (e.g. PHP-FPM). Some links are mandatory, some are optional. If a link is mandatory, a stack must specify which service from the stack should be used for a specific links. For example, in Drupal stack the PHP service requires _Database_ link, you can set it to use container-based _MariaDB_ or an external _Cloud MySQL_. 

You may change links in your stack from _"[Stack] > Configure > Stack services > [Service] > Links"_ page.

#### Volumes

You can change the size of volumes provided by a service for your stack from _"[Stack] > Configure > Stack services > [Service] > Volumes"_ page.

#### Settings

You can override settings provided by a service for your stack from _"[Stack] > Configure > Stack services > [Service] > Setting"_ page. Settings that source value from links cannot be edited.

#### Cron

You can create cron schedules for a service in your stack from _"[Stack] > Configure > Stack services > [Service] > Cron"_ page. Cron schedule must have a name, command and schedule. Schedule supports full crontab format (e.g. `0 0 * * *` for every day on midnight) and `@hourly`, `@daily` formats. A container with a specified command will be run according to the schedule. 

You can optionally limit a cron schedule to a certain environment type, when set the cron will run only on app instances that use the selected environment type.

### Tokens

You can add service-specific tokens for your stack from "[Stack] > Configure > Stack services > [Service] > Tokens" page. Such tokens will be added to a corresponding app service in app instances that use this stack revision.

Tokens can either have a plain value or a regular expression that will be used to generate a random secret value when an app services created/updated. You can use tokens in environment variables' value.

You can optionally limit a token to a certain environment type, when set tokens will be added only to app instances that use the selected environment type.

### Annotations

You can add service-specific annotations from "[Stack] > Configure > Stack services > [Service] > Annotations" page. Such annotations will be added to the corresponding app service's kubernetes resources during deployment in app instances that use this stack revision.

You can optionally limit an annotation to a certain environment type, when set annotations will be added only to app instances that use the selected environment type.

## Updates

When a service in a stack gets a new revision, your stack marked as outdated and can be updated. When you update a stack, the stack in your application will not be automatically updated, you can then upgrade your application stack for each instance individually. 

When you create a stack by adding from a catalog this stack marked as one that _has an origin_. Such stack can be additionally _synced with origin_. This may be useful if you want to get some updates from the stack in the catalog (not all stack updates done via services, sometimes there can be an update to a stack itself like addition of a new service or a new stack-wide environment variable).

## Sharing

Stack is a project's entity, it can be shared between multiple projects (with writable or read-only permissions) but must be attached to at least one project.

