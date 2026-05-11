# Service volume

A service volume represents persistent storage used by a service.

Volumes can optionally be shared with other services. In that case, the volume must reference a link, and the linked service provides the [distributed persistent storage](storage.md), for example through NFS, Rook, or Longhorn.

Service volumes can define a default size, which can then be overridden at the stack or app level.

When Wodby mounts a service volume directly, the volume must define `path` as the absolute mount path. This applies to shared volumes and volumes that reuse storage from a linked service with `from`. Helm-managed volumes that are not mounted directly by Wodby do not need `path`.

Service volumes are defined under the [`volumes` section](template.md#volumes) in a service template.
