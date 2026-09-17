# API keys

Create and manage API keys under `Account > API Keys` in the dashboard.

Every new API key must be scoped to one organization. The key can access only resources in that organization and only with the permissions of the user who created it. Choose an optional expiration when you create the key; its organization and expiration cannot be changed later.

The secret is shown only once, immediately after creation. Copy it to your password manager or CI secret store before leaving the page. The dashboard list shows the key's scope, creation date, last-used time, expiration, and status, but it cannot show the secret again. Delete a key to revoke it immediately.

!!! warning "Legacy global API keys"
    Existing global API keys continue to work across all organizations available to their owner, but new global keys cannot be created. Replace legacy global keys with organization-scoped keys when possible.

Organization-scoped keys authenticate API v3 requests through the `X-API-Key` header:

```shell
curl https://api.wodby.com/api/v3/user -H 'X-API-Key: YOUR_API_KEY'
```

Keep API keys out of source control, client-side code, logs, and other publicly accessible locations. Expired or deleted keys cannot authenticate new requests.
