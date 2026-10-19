# API keys

Create and manage API keys under `Account > API Keys` in the dashboard.

## Create a key

1. Open `Account > API Keys > Add a new key`.
2. Select the **Organization** and enter a **Name** for the key.
3. Choose **Expires**: Never, 1 month, 3 months, or 6 months. The default is 3 months.
4. Click **Create API key**, then copy the secret to your password manager or CI secret store.
5. Click **I have saved the key** to return to the list.

Every new API key must be scoped to one organization. The key can access only resources in that organization and only with the permissions of the user who created it. Its organization and expiration cannot be changed later.

The secret is shown only once, immediately after creation. Save it before leaving the page; the dashboard cannot show it again.

## Review and revoke keys

Open `Account > API Keys > List` to see each key's name, organization scope, creation date, last-used time, expiration, and status. Keys that have never been used show **Never** under Last used; keys without an expiration show **Never** under Expires.

To revoke a key, click its delete action and confirm. Deleted or expired keys cannot authenticate new requests. To replace a key, create a new one, update the integrations that use it, and delete the old key.

!!! warning "Legacy global API keys"
    Existing global API keys continue to work across all organizations available to their owner, but new global keys cannot be created. Replace legacy global keys with organization-scoped keys when possible.

## Use a key

Organization-scoped keys authenticate API v3 requests through the `X-API-Key` header:

```shell
curl https://api.wodby.com/api/v3/user -H 'X-API-Key: YOUR_API_KEY'
```

Keep API keys out of source control, client-side code, logs, and other publicly accessible locations. Expired or deleted keys cannot authenticate new requests.
