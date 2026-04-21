# Pusher

Pusher is available in Wodby as a `variable` provider. Use it when you want to inject Pusher application credentials into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Pusher App ID | Yes | `PUSHER_APP_ID` |
| Pusher Key | Yes | `PUSHER_KEY` |
| Pusher Secret | No | `PUSHER_SECRET` |
| Pusher Cluster | No | `PUSHER_CLUSTER` |

## Usage

After you create a Pusher integration and attach it to an app service or stack, Wodby injects the variables above into the container.
