# Stripe

Stripe is available in Wodby as a `variable` provider. Use it when you want to inject Stripe keys into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Publishable key | Yes | `STRIPE_PUBLISHABLE_KEY` |
| Secret key | No | `STRIPE_SECRET_KEY` |

## Usage

After you create a Stripe integration and attach it to an app service or stack, Wodby injects the variables above into the container.
