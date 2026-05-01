# Billing

## Plans

Live pricing is available at https://wodby.com/pricing.

Wodby has three plans.

### Developer

Free subscription designed for evaluation and development work.

Typical included capabilities:

- 10 app services
- 30 minutes of Wodby CI per month
- 5 GB of private Docker registry storage
- logs streaming
- stacks updates
- manual backups and imports
- technical domains with SSL
- community support

### Team

Designed for small teams and production workloads. Limits can be increased with addons.

Team includes everything in Developer, plus production-focused features such as:

- custom domains
- auto-renewed SSL certificates
- autoscaling tools
- auto backups
- scheduled cron jobs
- web shell for containers
- best-effort support
- 1000 compute credits per month for Wodby Cloud

Billing is per [app service](apps/services.md). On paid plans, usage is billed by app-service hours over the billing period.

### Enterprise

Designed for large workloads and teams. Custom pricing and limits. On-premises option available.

## What is billed separately

- App services on paid plans
- Addons usage above included amounts
- Wodby Cloud compute usage if you run workloads on Wodby Cloud
- Infrastructure costs from your cloud provider if you use managed Kubernetes, managed databases, or other resources in your own account

## Addons

Addons let you extend included limits and pay for extra usage when needed.

- Addons have some free number of units every billing cycle
- Addons are pay-as-you-go, and billing is calculated at the end of the cycle
- You are charged only for usage above the free included amount
- Free subscription is not eligible for exceeding addon limits
- You can set up usage limits for Wodby CI minutes in the billing settings

### Wodby CI minutes

[Wodby CI](cicd/wodby-ci.md) is the default CI system to build your applications, release artifacts, and run deployments.

Each billing cycle includes a free amount of build minutes. Additional usage is billed by total build minutes.

### Wodby registry storage

Wodby Registry is the default private Docker registry for images built and released during CI. Storage usage is billed by total GB-hours.

When you delete your app instance, we automatically delete all images associated with it.

You can selectively delete older builds to clean up docker images.

### Wodby cloud storage

Wodby Cloud Storage can be used for backups. Backup storage usage is billed by total GB-hours.

When you delete your app instance, we automatically delete all associated backups stored on Wodby Cloud storage.

You can selectively delete backups to clean up stored backup data.

### Wodby data transfer

Wodby data transfer is the total amount of data moved to and from Wodby Cloud Storage. It is billed by total transfer volume.

### Users

Extra organization users can be purchased as an addon. Usage is billed by total user-hours.

### Projects

Extra projects can be purchased as an addon. Usage is billed by total project-hours.
