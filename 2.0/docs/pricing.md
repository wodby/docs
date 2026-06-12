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
- $24 of Wodby compute per month

Billing is per [app service](apps/services.md). On paid plans, usage is billed by app-service hours over the billing period.

### Enterprise

Designed for large workloads and teams. Custom pricing and limits. On-premises option available.

## What is billed separately

- App services on paid plans
- Addons usage above included amounts
- Wodby Cloud compute usage if you run workloads on Wodby Cloud
- Infrastructure costs from your cloud provider if you use managed Kubernetes, managed databases, or other resources in your own account

Organization users and projects are included in your plan and are not billed separately.

## Addons

Addons let you extend included limits and pay for extra usage when needed.

- Addons have some free number of units every billing cycle
- Addons are pay-as-you-go, and billing is calculated at the end of the cycle
- You are charged only for usage above the free included amount
- Free subscription is not eligible for exceeding addon limits
- Paid subscriptions can use optional spending limits for the main plan and for individual addons in the billing settings

## Spending limits

From `Organization > Billing > Subscription`, paid subscriptions can set optional spending limits for:

- the main app-service plan usage
- individual addons such as Wodby CI minutes, registry storage, and Wodby compute

In practice:

- leaving the value empty means `Unlimited`
- the main plan limit cannot be set below the included app-service amount for that plan
- addon limits are configured separately per addon
- when a limit is reached, the billing UI shows that the limit was exceeded

On the free plan, usage above included addon amounts is not allowed. In that case you must either upgrade or wait for the next billing cycle when the addon is renewable.

### Wodby CI minutes

[Wodby CI](cicd/wodby-ci.md) is the default CI system to build your applications, release artifacts, and run deployments.

Each billing cycle includes a free amount of build minutes. Additional usage is billed by total build minutes.

### Wodby registry storage

Wodby Registry is the default private Docker registry for images built and released during CI. Storage usage is billed by total GB-hours.

When you delete your app instance, we automatically delete all images associated with it.

You can selectively void older build images to clean up docker images while keeping the build records.

### Wodby compute

Wodby Cloud is billed in dollars as Wodby compute usage.

Compute usage is based on the selected machine type, node count, persistent storage, and cluster infrastructure used during the billing period. Scalable Wodby Cloud clusters incur an additional cluster fee.

Paid plans include $24 of Wodby compute per month.
