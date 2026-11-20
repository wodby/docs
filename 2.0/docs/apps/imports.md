---
description: Import files or data into an app service from an uploaded archive, a public URL or a backup, including imports from another app.
---

# Application imports

If an application's stack includes services that provide [import functionality](../services/operations.md#imports), you can run imports for the corresponding app service.

There are two main import methods.

The source can be an uploaded archive, a public URL, or a completed backup from a compatible app service. When the
source app service has a usable backup preset, Wodby can also create a fresh backup to use for the import.

## Importing from another app

A backup-based import must stay within the destination app's [ownership boundary](../sharing.md#creation-import-and-copy-forms):

- the source and destination apps must belong to the same organization
- an organization-owned destination can import only from an organization-owned source
- for a project-owned destination, the source app must be owned by or shared with the destination's owner project, including when the source app is organization-owned

Your access to both apps through separate projects does not combine their resource boundaries. Share the source app
with the destination project before starting the import. You also need the `Back up`
[permission](../access-control.md#environment-permissions) on the source environment, both to use one of its existing
backups and to create a fresh one.

## 1. Simple files import

Wodby imports files directly into the running volume by unpacking the provided tar archive to the specified path.
The import replaces the volume's content: files that aren't in the archive are removed.

This method is not transactional.

## 2. Through init volume

Wodby mounts the import archive into the init volume provided by the service, and a container performs the import during startup. This pattern is commonly used for databases.

This method is transactional. Wodby starts a copy of the app service with a new persistent volume. If the import succeeds, Wodby redeploys the service using the new volume that contains the imported data.

For a container-based database service, the app's database user keeps its expected credentials and access after the
import. If an uploaded dump creates a same-named user or role with different credentials, the import task reports a credential conflict instead of replacing that account. Database dumps intended
for this workflow should normally contain the application database schema and data, not server-level user or role
definitions.

## K3s storage capacity preflight

Before an app-service import runs on K3s, its task checks the capacity of the destination volume.

A transactional init-volume import on the default local-path storage needs room for the replacement data volume and
a temporary 10 GiB import volume while the current volume still exists. The import stops before it starts when known
available capacity is insufficient or the node reports disk pressure.

For an in-place files import, Wodby cannot know the archive's expanded size in advance. It still checks for disk
pressure, but reports capacity as unverified and continues. The same applies when capacity cannot be read from the
cluster.

When the import uses a fresh backup of another app service, Wodby checks storage for both the backup and the import.

External database imports do not use this Kubernetes volume preflight.
