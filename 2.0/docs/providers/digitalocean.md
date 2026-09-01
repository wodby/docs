# DigitalOcean

## Auth

We provide authentication via OAuth2. Upon creating the integration and passing through the OAuth2 authentication flow you will be asked by DigitalOcean to select an appropriate team. All resources we create will be created under the selected team.

## DOKS

Wodby provides a native integration with DigitalOcean Kubernetes Service. 

- There's no multi-region cluster support
- We create a kubernetes cluster without a control plane's High Availability (DO charges extra for the HA cluster)
- We enable autoscaling by default unless the cluster is created as a single-node cluster
- We do not allow creating cluster with shared CPU nodes (standard) and require the minimum size of a node to be 2 CPUs and at least 4GB of RAM to avoid performance issues
- DOKS has a limit of maximum 25 nodes per cluster. If you need to increase this limit please contact DigitalOcean support, then contact us
- Node disk is not configurable upon creation
- We create a single load balancer per regular cluster and deploy Envoy Gateway for public app entrypoints
- In single-node mode, Wodby does not create a DigitalOcean Load Balancer. Public app traffic is routed directly to the cluster node IP, and the endpoint is still shown in Wodby as a public IP or hostname.

### Storage

Persistent storage is provided by DigitalOcean Block Storage through the cluster's selectable storage classes. Wodby
creates a new block storage volume for each persistent volume claim and uses the default class when no other class is
selected.

## Managed Database

Wodby provides a native integration with DigitalOcean Managed Database.

- We support MySQL and PostgreSQL
- Storage size is not configurable upon creation
- Database server is higly available
- There's no storage autoscaling support
- You can manage your DBs and users form Wodby dashboard

## Spaces

Wodby provides a native integration with DigitalOcean Spaces. You can use it to store your applications' backups.

- Wodby requests bucket-list access through OAuth so available Spaces buckets can be selected
- When configuring backups, select an available bucket or enter its exact name. If bucket discovery is unavailable,
  manual entry remains available. Wodby resolves the bucket's region automatically
- Wodby creates and manages Spaces access keys required for backup operations
