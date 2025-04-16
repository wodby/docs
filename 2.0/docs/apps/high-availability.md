# Applications High Availability

There are multiple layers of high availability for your applications:

## [Kubernetes cluster high availability](../kubernetes/high-availability.md)

Make sure you have at least two cluster nodes in at least two different availability zones and highly available control plane (usually HA by default or optionally for extra fee).

## Stateless app services

It's easy to scale stateless app services, just enough to have at least 2 replicas deployed.

## Stateful app services

You must make sure your service has high-availability deployment options because often single server and HA deployments differs a lot because HA setup is much more complicated and requires more resources.

Alternatively, you can choose to use managed services for some of your stateful services like [Managed Database](../databases/managed.md).

## Distributed storage

Not all distributed storages are highly available, make sure you choose a distributed storage that is highly available. Alternatively, you can choose to use managed distributed storage (e.g. AWS EFS) instead of container-based.
