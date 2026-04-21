# Service volume

A service volume represents persistent storage used by a service.

Volumes can optionally be shared with other services. In that case, the volume must reference a link, and the linked service provides the [distributed persistent storage](storage.md), for example through NFS, Rook, or Longhorn.

Service volumes can define a default size, which can then be overridden at the stack or app level.

Service volumes are defined under the [`volumes` section](template.md#volumes) in a service template.
