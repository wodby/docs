---
description: Wodby Registry is the private container registry for your application images. Repositories, included storage, image retention and authentication.
---

# Wodby Registry

Wodby Registry is the private container registry used to store your application images. It is available at `us-docker.wodby.com`.

Each billing cycle includes 5 GB of registry storage. Storage above that amount is billed at $0.15 per GB, see [billing](../pricing.md#wodby-registry-storage).

You can sign in to Wodby Registry with your Wodby account. See [Auth](#auth).

## Repositories

Wodby creates one repository per app environment, using this pattern:

```text
[org-name]/[app-name]-[app-environment-name]
```

!!! important
    Docker images that are no longer associated with existing app environments or builds are cleaned up automatically.

## Build image retention

Build images associated with an existing app environment remain available for reuse and rollback by default. To limit
their retention, open `CI/CD > Builds > Settings` in the app environment and configure **Auto-void images of unused
builds older than**.

Automatic build-image cleanup applies only to Wodby Registry. It never removes an image that is used by the current
runtime or referenced by an unfinished deployment. See [Application Builds](../apps/builds.md#automatically-void-old-build-images)
for the available periods, cleanup timing, and deployment safeguards.

## Auth

Run `docker login us-docker.wodby.com` to access images in your organization's namespace:

- Username: the primary email of your Wodby account.
- Password: your account password, or an [API key](../user/api-keys.md).

If your account uses [two-factor authentication](../user/security.md#two-factor-authentication), the registry does not
accept your password. Use an API key as the password instead.

An API key gives access to the images of the organization it was created for. To work with another organization's
images, sign in with an API key of that organization.
