# Service volume

Service volume is the representation of a persistent volume claim for a service. Volume can optionally be shared with other services, in this case it must have a link specified, a service from the link will implement the [distributed persistent storage](storage.md) like NFS server or Rook/Longhorn.

Service volume can have a default size that can be overridden on a stack or app level.

Service volumes defined under [`volumes` section](template.md#volumes) in a service template.
