# Wodby Registry

Wodby Registry is the private Docker registry used to store your application images. It is available at `us-docker.wodby.com`.

Each billing cycle includes 5 GB of registry storage. Storage above that amount is billed at $0.15 per GB, see [billing](../pricing.md#wodby-registry-storage).

You can authenticate to Wodby Registry using your Wodby account credentials.

## Repositories

Wodby creates one repository per app environment, using this pattern:

```text
[org-name]/[app-name]-[app-environment-name]
```

!!! important
    Docker images that are no longer associated with existing app environments or builds are cleaned up automatically.

## Auth

You can access images in your organization's namespace with your Wodby account credentials via `docker login us-docker.wodby.com`.
