# Pricing & Billing

## Plans

Actual prices can found at https://wodby.com/pricing.

Wodby Cloud version provides three subscription plans:

### Developer 

Free subscription. Designed to use for development purposes and trying out Wodby Platform, strict limits

### Team 

Designed for small teams and projects, more resources and features. Limits can be increased with addons. 

Billing per [app service replica](apps/services.md#replicas). Pay-as-you-go, we charge you for the number of app services replicase hours you used during the billing period. 

### Enterprise

Designed for big workloads and teams. Custom pricing and limits. On-premises option available.

## Addons

To better address resources usage and limits we provide addons.

- Addons have some free amount of units every billing cycle
- All addons are pay-as-you-go, you will be billed for the total amount of used resources at the end of the billing cycle
- You will be charged only for the amount of units used above the free included amount
- Free subscription is not eligible for exceeding addon limits
- You can set up usage limits for Wodby CI minutes in the billing settings

### Wodby CI minutes

[Wodby CI](cicd/wodby-ci.md) is the default CI system to build your applications, release artifacts (docker images) and run deployments. 

Some amount of free minutes included every billing. Pay-as-you-go, you will be billed for the total build minutes used at the end of the billing cycle. 

### Wodby registry storage

Wodby registry is the default private docker registry to store docker images built and released during CI process. We bill for storage used by your images in the Wodby registry. Pay-as-you-go, you will be billed for the total GB hours used at the end of the billing cycle. 

When you delete your app instance we automatically delete all images associated with it.

You can selectively delete older builds to clean up docker images.

### Wodby cloud storage

Wodby cloud storage is the cloud storage that can be used for backups. We bill for storage used by backups stored on Wodby Cloud. Pay-as-you-go, you will be billed for the total GB hours used at the end of the billing cycle.

When you delete your app instance we automatically delete all associated backups stored on Wodby Cloud storage.

You can selectively delete backups to clean up docker images.

### Wodby data transfer

Wodby data transfer is the total amount of data transferred to and from Wodby Cloud Storage. Pay-as-you-go, you will be billed for the total GB transferred used at the end of the billing cycle. 

### Users

Extra organization users can be purchased as an addon. Pay-as-you-go, you will be billed for the total user-hours used at the end of the billing cycle.

### Projects

Extra projects can be purchased as an addon. Pay-as-you-go, you will be billed for the total projects-hours used at the end of the billing cycle.
