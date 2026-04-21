# Provider vs Integration

Providers and integrations are related, but they are not the same thing.

If you keep one rule in mind, use this one:

- a **provider** is the template
- an **integration** is your actual connection created from that template

## Quick model

| Term | What it is | Example |
| --- | --- | --- |
| Provider | Wodby's definition of how to work with a third-party service | `AWS`, `GitHub`, `OpenAI` |
| Integration | Your configured connection created from a provider | `AWS production account`, `GitHub org connection`, `OpenAI team key` |
| Variable provider | A provider whose main job is to expose environment variables | `Sentry`, `Stripe`, or your own custom variable provider |
| Variable integration | A concrete integration created from a variable provider | `Stripe production keys`, `Sentry staging DSN` |

## How they relate

The usual flow is:

1. choose a provider
2. create an integration from that provider
3. assign the integration to one or more projects
4. use that integration from Kubernetes, databases, stacks, or app services

## Provider

A provider defines:

- required fields
- supported integration kinds or types
- auth method
- any variables the provider exposes
- any provider-specific setup rules

Providers are reusable product definitions, not your credentials.

## Integration

An integration is your actual configured object inside Wodby.

This is where you store:

- credentials
- account IDs
- DSNs
- API keys
- repository access details
- storage bucket access

Integrations are the objects you actually attach to apps, stacks, clusters, backups, and other workflows.

## Variable providers and variable integrations

Variable providers are useful when the result you want is a reusable set of environment variables rather than a full infrastructure integration.

Use a variable provider and integration when:

- you want to centralize third-party credentials
- the same values are reused across multiple apps or stacks
- Wodby does not yet ship a built-in provider for that service

Use plain app-service environment variables instead when the value is one-off and not worth centralizing.

## Examples

### Example 1: AWS

- Provider: `AWS`
- Integration: `AWS account for production`
- Result: can be used for Kubernetes, storage, or other AWS-backed workflows depending on the selected kinds

### Example 2: Sentry

- Provider: `Sentry`
- Integration: `Sentry for staging`
- Result: injects Sentry-related environment variables into the app services where you attach it

### Example 3: Custom variable provider

- Provider: `Acme internal APIs`
- Integration: `Acme production credentials`
- Result: exposes the environment variables you defined in that custom provider

## Related pages

- [Integrations overview](index.md)
- [Providers overview](../providers/index.md)
- [Integration types](types.md)
- [Variable integration](variable.md)
