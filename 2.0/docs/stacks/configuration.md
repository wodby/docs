# Stack Configuration

Unlike Wodby 1.0, there is no separate managed stack mode. Stacks are meant to be customized to your needs while still
receiving updates from the services they include.

## Environment Variables

You can add stack-wide environment variables from "[Stack] > Configure > Env vars". These values are applied to app
services deployed from that stack revision.

An environment variable can be marked as secret. Secret values are stored in a Kubernetes secret and are not shown in
the Wodby dashboard.

You can also limit a variable to a specific environment type.

## Annotations

You can add stack-wide annotations from "[Stack] > Configure > Annotations". These annotations are added to app
services deployed from that stack revision.

You can also limit an annotation to a specific environment type.

## Helm values

You can add stack-wide Helm values from "[Stack] > Configure > Helm values". These values are applied to app services
deployed from that stack revision and are useful when you need to override chart settings exposed by a service.

Each Helm value has a path-like name and a value. Values can be plain values, arrays, or objects.

Helm values can be stored as secrets, and you can optionally limit them to a specific environment type.

## Tokens

You can add stack-wide tokens from "[Stack] > Configure > Tokens". These tokens are available to app services created
from that stack revision.

Tokens can either store a fixed value or generate a secret value from a regular expression. You can reference tokens in
environment variable values.

You can also limit a token to a specific environment type.

## Stack Services

A stack always includes specific service revisions. When a service publishes a new revision, the stack can be updated to
use it.

Each service in a stack can be configured under "[Stack] > Configure > Stack services > [Service]". A service can be
enabled or disabled and marked as required or optional. Required services cannot be excluded during new app creation.

Only one service should be marked as main. If that service has an HTTP endpoint, the app's main technical domain will
target the main endpoint of the main app service.

If no service is marked as main, Wodby uses the first HTTP-capable service in the stack.

### Replicas

You can change the number of replicas per service. This is not available for external services.

### Integrations

If a service defines integrations in its template, you can preconnect compatible integrations from your project. For
example, a mail service can be configured with an SMTP integration so new app instances already have the relay set up.

Additionally, all non-external services can use [Variable](../integrations/variable.md) integrations.

### Environment Variables

You can add service-specific environment variables from _"[Stack] > Configure > Stack services > [Service] > Env vars"_.
These values are applied only to the corresponding app service.

An environment variable can be marked as secret. Secret values are stored in a Kubernetes secret and are not shown in
the Wodby dashboard.

You can also limit a variable to a specific environment type.

### Helm values

You can add service-specific Helm values from _"[Stack] > Configure > Stack services > [Service] > Helm values"_.
These values apply only to the selected service and are useful when one service needs a chart override without changing
the rest of the stack.

Each Helm value has a path-like name and a value. Values can be plain values, arrays, or objects.

Helm values can be stored as secrets, and you can optionally limit them to a specific environment type.

### Resources

For non-external services you can set up resource requests and limits from
_"[Stack] > Configure > Stack services > [Service] > Resources"_. These map to
[Kubernetes resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-limits-are-run).

#### Request

You can set CPU and memory requests. Requests help your cluster schedule workloads across nodes. If the cluster does
not have enough resources, deployments can stay pending. CPU requests are required for scalability.

#### Limit

You can set CPU and memory limits. Limits help control bursty workloads and reduce their impact on other services in
the same cluster.

### Options

Options represent different versions or variants of a service. A stack can limit which options are enabled, for
example to enforce compatibility or exclude end-of-life versions. You can change the default option and enabled
options from _"[Stack] > Configure > Stack services > [Service] > Options"_.

### Links

A service may provide a _link_, which represents a connection to another service. Some links are mandatory and some are
optional. If a link is mandatory, the stack must specify which service should satisfy it.

You can change links in your stack from _"[Stack] > Configure > Stack services > [Service] > Links"_.

### Volumes

You can change the size of volumes provided by a service from _"[Stack] > Configure > Stack services > [Service] > Volumes"_.

### Settings

You can override settings provided by a service from _"[Stack] > Configure > Stack services > [Service] > Settings"_.
Settings whose value comes from links cannot be edited.

### Configs

If a service defines [configs](../services/configs.md), the stack can provide default overrides for them. These
defaults apply to app instances created from the stack revision and can still be overridden later at the app level.

### Cron

You can create cron schedules for a service in your stack from _"[Stack] > Configure > Stack services > [Service] > Cron"_.
Each schedule must have a name, command, and schedule. Use standard five-field crontab syntax such as
`0 0 * * *`. Cron schedules cannot run more often than once per hour.

You can also limit a cron schedule to a specific environment type.

### Tokens

You can add service-specific tokens from "[Stack] > Configure > Stack services > [Service] > Tokens". These tokens are
available to the corresponding app service.

Tokens can either store a fixed value or generate a secret value from a regular expression. You can reference tokens in
environment variable values.

You can also limit a token to a specific environment type.

### Annotations

You can add service-specific annotations from "[Stack] > Configure > Stack services > [Service] > Annotations". These
annotations are added only to the corresponding app service.

You can also limit an annotation to a specific environment type.

### Derivatives

If a service defines [derivatives](../services/derivatives.md), the stack can include those derivative services and
decide whether they are enabled or required by default.
