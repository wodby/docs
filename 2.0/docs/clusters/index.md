# Clusters

## Overview

Wodby 2.0 works only with Kubernetes clusters. You can connect your Kubernetes cluster from a cloud provider that offers managed Kubernetes services, e.g. Google Kubernetes Engine (GKE), DigitalOcean Kubernetes (DOKS), Elastic Kubernetes Service (EKS) from AWS, etc. To create a cluster you should first connect your account from appropriate cloud provider to Wodby by creating a new integration with kubernetes kind.

When you delete a cluster from Wodby we will also delete it from your cloud provider. 

!!! danger "Do not modify your cluster from cloud provider panel"
    Clusters created from Wodby should not be modified directly from a cloud provider panel. This will lead to unexpected errors. 