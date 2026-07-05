# Wodby API keys

Wodby API keys are created from [User settings > API keys](../user/api-keys.md).

Each key belongs to a single organization and authenticates as the user who created it. In practice, that means:

- the key is scoped to one organization
- requests made with the key run with that user's permissions inside that organization
- the backend resolves the organization context from the key itself

Use API keys for external automation against the public REST API. Send the key in the `X-API-KEY` header.

## What you choose when creating a key

- organization
- description
- expiration: `No expiration`, `1 month`, `3 months`, or `6 months`

## Important behavior

- The token value is shown only once after creation.
- The list later shows metadata such as creation time, last use, and expiry, but not the token itself.
- You can revoke keys at any time from the same user settings page.
- The backend updates `last use` when the key is used successfully.

## Typical uses

- authenticating automation against the Wodby API
- using the [Wodby CLI](cli.md)
- scripting organization-specific operational tasks

## Header example

```bash
curl -sS \
  -H "X-API-KEY: ${WODBY_API_KEY}" \
  https://api.wodby.com/v1/orgs
```

## Recommended practices

- create separate keys per automation or CI system
- set an expiration unless the workflow genuinely needs a long-lived key
- store the value in your secrets manager, not in repository files
- rotate keys instead of reusing one key everywhere
- revoke keys that are no longer attached to an active workflow

See [User API keys](../user/api-keys.md) for key management in the dashboard.

## Related pages

- [Wodby API](api.md)
- [Wodby CLI](cli.md)
- [User API keys](../user/api-keys.md)
