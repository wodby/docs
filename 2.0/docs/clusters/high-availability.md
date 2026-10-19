# Cluster high availability

## Overview

To ensure high availability of the kubernetes cluster, you need to ensure that the control plane is highly available and have at least two nodes across different availability zones.

[Managed kubernetes](managed.md) services usually provide highly available control plane (for a fee, like GKE, AKS, EKS) or an option to enable high availability for the control plane (DigitalOcean).

Not all managed kubernetes services provide option to use multiple availability zones.

Clusters created with `Single-node cluster` are not highly available. They have one worker node, so node maintenance or failure can interrupt applications.

## Multi-regional deployment

A Wodby app environment runs on one Kubernetes cluster. Wodby does not currently orchestrate one app environment across
multiple regions.

For a multi-region architecture, use separate app environments on clusters in the required regions and design the
application's data replication, traffic failover, and consistency model explicitly. Wodby does not automatically
synchronize application data or switch external traffic between those environments.
