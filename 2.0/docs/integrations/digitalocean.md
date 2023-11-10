# DigitalOcean

## Auth

We provide authentication via OAuth2. Upon creating the integration and passing through the OAuth2 authentication flow you will be asked by DigitalOcean to select an appropriate team. All resources we create will be created under the selected team.

## DOKS

Wodby provides a native integration with DigitalOcean Kubernetes Service. 

- There's no multi-region cluster support
- We create a kubernetes cluster without a control plane's High Availability (DO charges extra for the HA cluster)
- We always enable autoscaling by default
- We do not allow creating cluster with shared CPU nodes (standard) and require the minimum size of a node to be 2 CPUs and at least 4GB of RAM to avoid performance issues
- DOKS has a limit of maximum 25 nodes per cluster. If you need to increase this limit please contact DigitalOcean support, then contact us
- Node disk is not configurable upon creation
- We create a single load balancer per cluster and deploy an Ingress Nginx controller to manage SSL certificates

### Storage

Persistent storage is provided by DigitalOcean Block Storage via the default storage class. We create a new block storage volume for each persistent volume claim. 
