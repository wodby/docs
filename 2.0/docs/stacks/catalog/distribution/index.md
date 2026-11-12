---
description: Run a private CNCF Distribution Registry v3 on Wodby with the Distribution Registry catalog stack, basic authentication and an optional Valkey cache.
---

# Distribution Registry

The Wodby Distribution Registry catalog stack runs a private CNCF Distribution Registry v3 with an optional Valkey
metadata cache. The current services and defaults are documented in
[`wodby/stack-distribution`](https://github.com/wodby/stack-distribution).

## Sign in

Basic authentication is on by default. The account is `admin`. Its password is the `password` token on the registry app
service's **Configuration > Tokens** tab. The registry listens on port `5000` over HTTP, so Wodby generates a technical
route for it. See [Endpoints](../../../apps/endpoints.md#technical-domains).

To use the registry for your Wodby builds, create a Distribution Registry integration with the registry's hostname and
this account. See [Distribution Registry](../../../providers/distribution.md). The host must be reachable from the public
internet.

Delegated token authentication is optional. It needs a compatible `distribution-auth` service linked to the registry in
a custom version of the stack.

## Choose storage

By default the registry stores images on its persistent volume. The stack adds a 20 GiB **Registry data** volume.

For object storage, attach one integration to the registry app service under **Connections > Integrations**:

- **Google Cloud Storage**: asks for a bucket and a service-account key.
- **Amazon S3**: asks for a bucket, an access key, a secret key and a region.

Attach at most one storage integration. See [Integrations tab](../../../apps/services.md#integrations-tab).

## Replicas and zero-downtime releases

The registry can run several replicas. Releases start a new replica before stopping the old one. Both need the same
registry storage:

- Google Cloud Storage and Amazon S3 give every replica the same storage.
- A filesystem volume works only if the storage class can mount the same volume in the old and the new pod. A
  `ReadWriteOnce` volume may stall the rollout. Use object storage when releases must not cause downtime.

## Metadata cache

The **Registry metadata cache** is a Valkey service linked to the registry through its `redis` link. It is optional and
enabled by default. It is a disposable cache: it writes nothing to disk, holds up to 256 MB and evicts the least recently
used keys. You can exclude it when you create the app. The link also accepts a Redis service.

## Backups

The registry service has no backup or import support.
