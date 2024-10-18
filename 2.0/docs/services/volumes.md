# Service volume

Service volume is the representation of a persistent storage required by a service. Volume can optionally be shared, in this case it must have a link specified, a service from the link will implement the distributed persistent storage like NFS server or Rook/Longhorn. 

Service volume can have a default size that can be overridden on a stack or app level.
