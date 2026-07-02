# Stack Configuration

Unlike Wodby 1.0, there is no separate managed stack mode. Stacks are meant to be customized to your needs while still
receiving updates from the services they include.

## Draft revisions

Stack configuration changes are saved to an unpublished draft revision. The currently published revision remains active
for existing app instances until you publish the draft.

Use `Publish draft` when you want the draft to become a real stack revision. At that point, app instances using older
published revisions can become outdated and can be upgraded from `Stack > Operations`.

Use `Discard` to delete the draft and abandon unpublished stack changes. If there is no draft, the stack has no
unpublished configuration changes.

Changing the stack title is part of the draft revision. Changing the stack machine name is a stack-level change and
applies immediately.

## Environment Variables

Add stack-wide environment variables from `Stack > Configure > Env vars`. These values apply to app services deployed from that stack revision.

An environment variable can be marked as secret. Secret values are stored in a Kubernetes secret and are not shown in the Wodby dashboard.

You can also limit a variable to a specific environment type.

## Annotations

Add stack-wide annotations from `Stack > Configure > Annotations`. These annotations are added to app services deployed from that stack revision.

You can also limit an annotation to a specific environment type.

## Helm values

Add stack-wide Helm values from `Stack > Configure > Helm values`. These values apply to app services deployed from that stack revision and are useful when you need to override chart settings exposed by a service.

Each Helm value has a path-like name and a value. Values can be plain values, arrays, or objects.

Helm values can be stored as secrets, and you can optionally limit them to a specific environment type.

## Tokens

Add stack-wide tokens from `Stack > Configure > Tokens`. These tokens are available to app services created from that stack revision.

Tokens can either store a fixed value or generate a secret value from a regular expression. You can reference tokens in
environment variable values.

You can also limit a token to a specific environment type.

Stack-wide tokens override service-defined tokens with the same name and environment type. A stack-service token with
the same name and environment type overrides the stack-wide token for that specific stack service.

## Stack Services

A stack always includes specific service revisions. When a service publishes a new revision, the stack can be updated to
use it.

This is a stack update: Wodby updates the stack service revisions in a new stack revision. App instances that use the
stack are upgraded to that published revision separately. See [Stack updates](updates.md) for update paths such as
service revision updates, Git updates, and sync with origin.

Each service in a stack can be configured under "[Stack] > Configure > Stack services > [Service]". A service can be
enabled or disabled and marked as required or optional. Required services cannot be excluded during new app creation.

You can pin a stack service to its current service revision. Pinned stack services are skipped by manual and automatic
stack service revision updates, and they do not make the stack appear outdated when the underlying service publishes a
new revision. Derivative stack services inherit the pin state from their parent service.

Only one HTTP-capable service can be marked as main. Services without HTTP endpoints cannot be main. The main stack
service controls which app service receives the app instance's main technical route, which targets the main endpoint of
the main app service.

If no service is marked as main and the stack has HTTP-capable services, Wodby uses the first HTTP-capable service in
the stack. This fallback also applies when you add or sync an HTTP-capable service into a stack that currently has no
main service. Stacks without HTTP-capable services can have no main service.

### Replicas

You can set the number of replicas per service. This is not available for external services.

### Integrations

If a service defines integrations in its template, you can preconnect compatible integrations from your project. For
example, a mail service can be configured with an SMTP integration so new app instances already have the relay set up.

Additionally, all non-external services can use [Variable](../integrations/variable.md) integrations.

### Environment Variables

Add service-specific environment variables from `Stack > Configure > Stack services > [Service] > Env vars`. These values apply only to the corresponding app service.

Variables can be global for the whole service or scoped to a specific workload and container. If no target is set, the
variable applies to all containers in that app service.

An environment variable can be marked as secret. Secret values are stored in a Kubernetes secret and are not shown in the Wodby dashboard.

You can also limit a variable to a specific environment type.

### Helm values

Add service-specific Helm values from `Stack > Configure > Stack services > [Service] > Helm values`. These values apply only to the selected service and are useful when one service needs a chart override without changing the rest of the stack.

Each Helm value has a path-like name and a value. Values can be plain values, arrays, or objects.

Helm values can be stored as secrets, and you can optionally limit them to a specific environment type.

### Resources

For non-external services, configure resource requests and limits from `Stack > Configure > Stack services > [Service] > Resources`. These map to [Kubernetes resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-limits-are-run).

Resources are set per workload and container defined by the service manifest.

#### Request

Set CPU and memory requests. Requests help the cluster schedule workloads across nodes. If the cluster does not have enough capacity, deployments can stay pending. CPU requests are required for autoscaling.

#### Limit

Set CPU and memory limits. Limits help control bursty workloads and reduce their impact on other services in the same cluster.

### Options

Options represent different versions or variants of a service. A stack can limit which options are enabled, for
example to enforce compatibility or exclude end-of-life versions. You can change the default option and enabled options from `Stack > Configure > Stack services > [Service] > Options`.

An `EOL` flag on a stack means at least one enabled stack service defaults to an end-of-life version. If you do not see
the expected replacement versions or exact EOL dates, first [update the stack service revisions](updates.md#update-stack-service-revisions).

### Links

A service may provide a _link_, which represents a connection to another service. Some links are mandatory and some are
optional. If a link is mandatory, the stack must specify which service should satisfy it.

Change links from `Stack > Configure > Stack services > [Service] > Links`.

### Volumes

Change service volume sizes from `Stack > Configure > Stack services > [Service] > Volumes`.

### Settings

Override service settings from `Stack > Configure > Stack services > [Service] > Settings`. Settings whose value comes from links cannot be edited.

### Configs

If a service defines [configs](../services/configs.md), the stack can provide default overrides for them. These
defaults apply to app instances created from the stack revision and can still be overridden later at the app level.
Stack overrides replace only the config content or disable the config. The service template still defines whether the
config is delivered via Helm, mounted from a generated ConfigMap, or exposed by filename only.

### Cron

Create cron schedules for a service from `Stack > Configure > Stack services > [Service] > Cron`. Each schedule must have a name, command, and schedule. Use standard five-field crontab syntax such as `0 0 * * *`. Cron schedules cannot run more often than once per hour.

You can also limit a cron schedule to a specific environment type.

### Tokens

Add service-specific tokens from `Stack > Configure > Stack services > [Service] > Tokens`. These tokens are available to the corresponding app service.

Tokens can either store a fixed value or generate a secret value from a regular expression. You can reference tokens in
environment variable values.

You can also limit a token to a specific environment type.

Stack-service tokens take precedence over both service-defined and stack-wide tokens with the same name and environment
type.

### Annotations

Add service-specific annotations from `Stack > Configure > Stack services > [Service] > Annotations`. These annotations are added only to the corresponding app service.

You can also limit an annotation to a specific environment type.

### Derivatives

If a service defines [derivatives](../services/derivatives.md), the stack can include those derivative services and
decide whether they are enabled or required by default.
