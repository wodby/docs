# Azure

## Auth

We provide authentication via OAuth2. After creating the integration and passing through the OAuth2 authentication flow you will be asked to select an appropriate Azure subscription. All resources we create will be created under the selected subscription.

## AKS

Wodby provides a native integration with Azure Kubernetes Service. We use deployment template to create a cluster, its network and node pools. 

- We place all resources we create in a resource group named `wodby-[your-wodby-org-name]-[region]`
- AKS cluster we create always deployed with multi-az high availability in a chosen region
- We set a limit of 50 pods per node by default
- Since AKS cluster comes with a metrics server we use it for the basic Wodby kubernetes monitoring
- We create a single load balancer per cluster and deploy an Ingress Nginx controller to manage SSL certificates
- We disable native Azure monitoring when creating a cluster

We support the following regions:

- south africa north
- east asia
- south east asia
- australia central
- australia southeast
- australia east
- brazil south
- canada east
- canada central
- china east2
- china north2
- north europe
- west europe
- france central
- germany west central
- central india
- south india
- japan east
- japan west
- korea central
- norway east
- sweden central
- switzerland north
- uae north
- uk south
- uk west
- east us
- east us 2
- west us
- west us 2
- west us 3
- central us
- north central us
- south central us
- west central us

### Storage

Persistent storage is provided by Azure Managed Disk via the default storage class. We create a new block storage volume for each persistent volume claim.

## Databases

Wodby provides a native integration with Azure Databases

- We support MySQL (with flexible option), MariaDB and PostgreSQL (flexible option)
- Databases can be resided with a EKS cluster created under the same integration
- Storage size can be configured upon creation and storage autoscaling can be enabled
- You can manage your DBs and users form Wodby dashboard

## Blob storage

Integration with Azure Blob Storage is coming soon...
