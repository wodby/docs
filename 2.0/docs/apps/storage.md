# Application Persistent Storage

Persistent storage options depend on the type of cluster you run: [managed Kubernetes](../kubernetes/managed.md) or [K3S](../kubernetes/k3s.md).

## Storage types

### Block storage

Block storage is available on managed Kubernetes clusters. It is usually provided by the cloud platform and exposed through a storage class already configured in the cluster.

Block storage is typically single-writer and attached to one node at a time.

### Local storage

Local storage is typical for K3S clusters. By default, persistent volume claims use storage from the server where the app service is running.

### Distributed storage

#### Container-based

Some workloads need shared storage with multiple writers, especially in scaled or highly available setups. For those cases, Wodby provides [storage services](../services/storage.md).

The simplest container-based option is an NFS server. It is easy to use, but it is not highly available on its own. In this setup, the NFS server stores its data on local or block storage, depending on the cluster type, and then exposes a storage class for other services to use.

Services that require distributed storage have [volumes](../services/volumes.md) defined with a mandatory link to reference a storage service.

#### Managed

You can also use a third-party distributed storage system such as AWS EFS when your infrastructure supports it.
