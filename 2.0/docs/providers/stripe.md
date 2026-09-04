# Stripe

Stripe is available in Wodby as a `variable` provider. Use it when you want to inject Stripe keys into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Publishable key | Yes | `STRIPE_PUBLISHABLE_KEY` |
| Secret key | No | `STRIPE_SECRET_KEY` |
| Webhook signing secret | No | `STRIPE_WEBHOOK_SIGNING_SECRET` |

Use the webhook signing secret only when the application verifies events delivered to a Stripe webhook endpoint. Each
endpoint has its own signing secret. Wodby stores the secret key and webhook signing secret as secrets.

See [Stripe API keys](https://docs.stripe.com/keys) and
[Stripe webhook signature verification](https://docs.stripe.com/webhooks/signature).

## Usage

After you create a Stripe integration and attach it to an app service or stack, Wodby injects the variables above into the container.
