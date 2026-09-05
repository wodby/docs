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

## Build image retention

Build images associated with an existing app environment remain available for reuse and rollback by default. To limit
their retention, open `CI/CD > Builds > Settings` in the app environment and configure **Automatically delete build
images after**.

Automatic build-image cleanup applies only to Wodby Registry. It never removes an image that is used by the current
runtime or referenced by an unfinished deployment. See [Application Builds](../apps/builds.md#automatically-delete-old-build-images)
for the available periods, cleanup timing, and deployment safeguards.

## Auth

You can access images in your organization's namespace with your Wodby account credentials via `docker login us-docker.wodby.com`.
