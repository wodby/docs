# OVH

OVHcloud keeps three separate account systems. An account belongs to the one it was opened with and can sign in only
there, so Wodby has one provider for each:

| Provider | Use it when your OVHcloud account | Sign-in |
| --- | --- | --- |
| **OVH EU** | was opened with a European OVHcloud entity | `www.ovh.com` |
| **OVH CA** | was opened with OVHcloud Canada, which also serves Asia-Pacific and the Americas outside the United States | `ca.ovh.com` |
| **OVH US** | is an OVHcloud US account | `us.ovhcloud.com` |

Pick the provider that matches your account, not the data center you want. An EU or CA account can create clusters
in any region OVHcloud offers it, including regions on another continent. Data centers in the United States are
available to OVH US accounts only. If sign-in rejects a valid login, the account most likely belongs to another
provider in the table.

The three providers work the same way; everything below applies to each.

## Auth

Authentication uses OAuth2. Create an integration with the provider that matches your account and sign in at
OVHcloud. Then select an OVHcloud Public Cloud project to finish the integration. All resources Wodby creates are
created in that project.

## Kubernetes

Wodby provides integration with OVH Managed Kubernetes service. 

- OVH does not support highly available multi-AZ clusters
- We always enable autoscale for the cluster
- We disable `AlwaysPullImages` plugin
- We use the metrics server that comes by default for the basic Wodby kubernetes monitoring
- Node disk cannot be configured upon creation
- We create a single load balancer per cluster and deploy Envoy Gateway for public app entrypoints
- You can choose a [billing option: hourly or monthly](#billing) 

#### Supported regions

Wodby offers the regions where OVHcloud provides Managed Kubernetes for the selected project. Which ones you see
depends on your account:

- OVH EU and OVH CA: for example BHS, DE, GRA, SBG5, SGP, SYD, UK and WAW
- OVH US: US-EAST-VA and US-WEST-OR

### Billing

There are two billing options for OVH Kubernetes: hourly and monthly.

Hourly is more expensive than monthly. Useful for testing or when number of nodes will reduce significantly with autoscaling. 

Monthly is cheaper than hourly. Useful when autoscaling disabled or number of nodes not reduced significantly. Each time a node created via auto-scaling, OVH will bill you for one node immediately on a pro rata basis for the remaining time in the current month.

For more details please refer to the official OVH documentation.

### Storage

Persistent storage is provided by OVH Public Cloud Block Storage through the cluster's selectable storage classes.
Wodby creates a new block storage volume for each persistent volume claim and uses the default class when no other
class is selected.
