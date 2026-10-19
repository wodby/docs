# LaunchDarkly

LaunchDarkly is available in Wodby as a `variable` provider. Use it to inject a server-side LaunchDarkly SDK key into
app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| SDK key | Yes | `LD_SDK_KEY` |

Wodby stores the SDK key as a secret.

## Usage

After you create a LaunchDarkly integration and attach it to an app service or stack, Wodby injects `LD_SDK_KEY` into
the container.
