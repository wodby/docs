# OVH

## Auth

We provide authentication via OAuth2. After creating the integration and passing through the OAuth2 authentication flow you will be asked to select an appropriate OVH project. All resources we create will be created under the selected project.

## Kubernetes

Wodby provides integration with OVH Managed Kubernetes service. 

- OVH does not support highly available multi-AZ clusters
- We always enable autoscale for the cluster
- We disable `AlwaysPullImages` plugin
- We use the metrics server that comes by default for the basic Wodby kubernetes monitoring
- Node disk cannot be configured upon creation
- We create a single load balancer per cluster and deploy an Ingress Nginx controller to manage SSL certificates  
- You can choose a [billing option: hourly or monthly](#billing) 

#### Supported regions

We support the following OVH regions:

- BHS
- DE
- GRA
- SBG5
- SGP
- SYD
- UK
- WAW

### Billing

There are two billing options for OVH Kubernetes: hourly and monthly.

Hourly is more expensive than monthly. Useful for testing or when number of nodes will reduce significantly with autoscaling. 

Monthly is cheaper than hourly. Useful when autoscaling disabled or number of nodes not reduced significantly. Each time a node created via auto-scaling, OVH will bill you for one node immediately on a pro rata basis for the remaining time in the current month.

For more details please refer to the official OVH documentation.

### Storage

Persistent storage is provided by OVH Public Cloud Block Storage via the default storage class. We create a new block storage volume for each persistent volume claim.
