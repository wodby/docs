# Azure

## Auth

We provide authentication via OAuth2. After creating the integration and passing through the OAuth2 authentication flow you will be asked to select an appropriate Azure subscription. All resources we create will be created under the selected subscription.

## AKS

Wodby provides a native integration with Azure Kubernetes Service. We use deployment template to create a cluster, its network and node pools. 

- We place all resources we create in a resource group named `wodby-[your-wodby-org-name]-[region]`
- AKS cluster we create always deployed with multi-az high availability in a chosen region
- New clusters use Azure CNI Overlay with the AKS-managed Cilium dataplane and NetworkPolicy engine
- We set a limit of 50 pods per node by default
- Since AKS cluster comes with a metrics server we use it for the basic Wodby kubernetes monitoring
- We create a single load balancer per cluster and deploy Envoy Gateway for public app entrypoints
- We disable native Azure monitoring when creating a cluster

### Networking

New AKS clusters created by Wodby use Azure CNI Overlay. Pods receive addresses from the cluster's overlay network rather
than consuming IP addresses from the Azure virtual network subnet. The pod address range is `10.244.0.0/16`, while the
Kubernetes service address range is `10.0.0.0/16`.

AKS manages the Cilium dataplane and uses Cilium to enforce the app environment network policies created by Wodby. This does
not install a separate Wodby-managed Cilium release in the cluster.

This networking configuration applies to newly created clusters. Existing kubenet clusters are not migrated
automatically because changing an AKS cluster's networking model is a separate, disruptive operation. Legacy or imported
AKS clusters remain excluded from Wodby's app environment network policies when their enforcement capability is unknown.

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

Persistent storage is provided by Azure Managed Disk through the cluster's selectable storage classes. Wodby creates a
new block storage volume for each persistent volume claim and uses the default class when no other class is selected.

## Databases

Wodby provides a native integration with Azure Databases

- We support MySQL and PostgreSQL flexible versions
- MariaDB and single-server MySQL/PostgreSQL are not supported because Azure is retiring them
- Storage size can be configured upon creation and storage autoscaling can be enabled
- You can manage your DBs and users from Wodby dashboard
- Residing an Azure database with an AKS cluster is not currently supported

## Blob storage

Wodby provides a native integration with Azure Blob Storage. You can use it to store your applications' backups.

- Wodby requests storage-account listing through OAuth so available Blob containers can be selected
- When configuring backups, select an available container or enter it in the format `storage-account/container`. If
  container discovery is unavailable, manual entry remains available
- You do not need to select a region separately when configuring backups
- Supported storage classes: `hot`, `cool`, `cold`, `archive`
- The storage class override is optional. If you leave it empty, the bucket's default storage class will be used
