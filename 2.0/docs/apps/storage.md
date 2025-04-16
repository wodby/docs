# Applications persistent storage

Depending on your Kubernetes cluster deployment type ([managed](../kubernetes/managed.md) vs [K3S](../kubernetes/k3s.md)) there are different methods to store your application data persistently.

## Storage types

### Block storage

Available only for managed Kubernetes clusters, single-write. Usually offered by cloud providers as a managed service and already have storage class defined in your Kubernetes cluster. Block storage is a low-level storage that is attached to a single node.

### Local storage

Only for K3S clusters. By default, persistent volumes claims will take a local storage from the server where the app service is running.

### Distributed storage

#### Container-based

For scaled stateless services and for high-available deployments it's often mandatory to have a distributed storage to provide a multiple writes. For such cases Wodby provides [storage services](../services/storage.md), the simplest container-based implementation is an NFS server (although it's not highly available), in such setups NFS server uses a local or block storage (depending on your Kubernetes cluster deployment) to retain data and will provide a storage class.

Services that require distributed storage have [volumes](../services/volumes.md) defined with a mandatory link to reference a storage service.

#### Managed

Alternatively, it's possible to use a third-party distributed storage, e.g. AWS EFS, that is already highly available. 
