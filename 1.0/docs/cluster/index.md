# Managed Kubernetes cluster

## Overview

In addition to our single server infrastructure we offer a Kubernetes cluster solution. Currently, we offer cluster setup only for public clouds (AWS, GCP, Azure). Only specific stacks / services provided by Wodby are suitable for cluster deployment.

Setup and maintenance of the cluster is significantly more complex and expensive than a single-server setup. Normally we recommend cluster setups only if you need one of the following:

### Scalability

If you're not sure whether a single server is enough to handle your load, this probably means you don't need a cluster.

There are two types of scalability for different services of your stack:

1. Stateless services. These services don't care how many replicas are running and on which node (have no state). Can be flexibly scheduled across a pool of auto-scaled nodes. Stateless services can be scaled manually (# of replicas) or automatically (based on resources consumption). Examples: HTTP servers, PHP-FPM.
2. Stateful services. Run on specific nodes (have state) and require additional individual configuration for scalability (read replicas, sharding). Examples: any DBMS, Elasticsearch. Usually public clouds provide stateful services that can be scaled without manual configuration (e.g. AWS RDS, ElastiCache).

### High availability

HA setup guarantees that your application will recover if one of infrastructure services goes down. Services can be restored rapidly but not instantaneously. Suitable for applications that must be restored quickly and can withstand a short interruption should a failure occur.

* Stateless services configured for auto scheduling across a pool of nodes. New nodes in a pool will spun up automatically when requested.
* Stateful services configured for high availability (master-master, master-slave setup) or replaced by public cloud managed services with built-in high availability (e.g. AWS RDS instead of Galera Cluster).

High availability usually implies that the cluster deployed across 2 or more availability zones. 

### Fault tolerance

A fault-tolerant environment has no service interruption but a significantly higher cost. We run additional services replicas in multiple availability zones (inside the same region) for redundancy. The chance that two (or more) availability zones simultaneously goes down is extremely low but for extra high availability, infrastructure can be deployed across multiple regions.

### Supported Public Clouds

* AWS EKS
* GCP GKE
* Azure AKS

## Request cluster

We no longer accept applications for cluster deployments. Deployment of scalable managed clusters is now part of [Wodby 2.0](https://wodby.com/blog/wodby-2), fully automated and available for everyone.
