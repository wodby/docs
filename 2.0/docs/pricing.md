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
- app instance pausing
- auto backups
- scheduled cron jobs
- web shell for containers
- best-effort support
- $30 of Wodby Cloud usage per month

The Team plan has a $48 minimum for each monthly billing cycle. It includes up to 24 billable
[app services](apps/services.md). Capacity above the included amount is billed at the current rate shown on the
[pricing page](https://wodby.com/pricing).

App-service capacity is based on the current number of billable app services, not the highest count reached during the
cycle. When that number changes, Wodby prorates the capacity charge for the portion of the billing cycle during which
each quantity applied. The $48 plan minimum is not prorated when app-service usage falls below 24.

For example, if an organization has 30 billable app services for half of its billing cycle and 20 for the other half,
the base $48 still applies for the full cycle. Only the six services above the included 24 are charged for half of the
cycle.

### Enterprise

Designed for large workloads and teams. Custom pricing and limits. On-premises option available.

## What is billed separately

- App services on paid plans
- Addons usage above included amounts
- Wodby Cloud usage if you run workloads on Wodby Cloud
- Infrastructure costs from your cloud provider if you use managed Kubernetes, managed databases, or other resources in your own account

Organization users and projects are included in your plan and are not billed separately.

## Addons

Addons let you extend included limits and pay for extra usage when needed.

- Addons have some free number of units every billing cycle
- Addons are pay-as-you-go, and billing is calculated at the end of the cycle
- You are charged only for usage above the free included amount
- Free subscription is not eligible for exceeding addon limits
- Organization owners on paid subscriptions can use optional spending limits for the main plan and for individual addons in the billing settings

## Spending limits

From `Organization > Billing > Subscription`, organization owners on paid subscriptions can set optional spending limits for:

- the main app-service plan usage
- individual addons such as Wodby CI minutes, registry storage, and Wodby Cloud usage

In practice:

- leaving the value empty means `Unlimited`
- the main plan limit cannot be set below the included app-service amount for that plan
- addon limits are configured separately per addon
- operations that would exceed a limit can be blocked, and the billing UI shows that the limit was exceeded

Only organization owners can change subscription settings, open the customer portal, downgrade, upgrade, or update spending limits. Organization admins and support users can view billing information but cannot modify it.

On the free plan, usage above included addon amounts is not allowed. In that case you must either upgrade or wait for the next billing cycle when the addon is renewable.

## Downgrading a paid subscription

When you downgrade a paid subscription, the downgrade is scheduled for the end of the current billing cycle. The existing paid billing period continues for billing and existing resource usage until the current period ends, and the organization moves to the free Developer plan after that.

Usage-based charges can still accrue until the end of the billing cycle. The final invoice can include addon usage and Wodby Cloud usage above the included amounts for the period.

After a downgrade is scheduled:

- you can continue using existing resources until the billing period ends
- usage-based addons can continue to accrue charges until the period ends
- organization owners can still update spending limits
- new paid-only features and capacity above the Developer plan limit are not available

To schedule a downgrade, the organization must already fit the Developer plan limits and must not depend on paid-only
features. App instance pausing is a paid feature, so no instance can be `Pausing` or `Paused` when a downgrade is
scheduled. If an instance is `Pausing`, wait for it to reach `Paused`; then open **Apps > your app > your instance >
Settings > Pause & Resume**, select **Resume app instance**, and retry the downgrade after it finishes. The downgrade
error identifies each affected app and instance.

If autoscaling is configured, the downgrade error identifies the affected app, instance, and service. Open each
service from **Apps > your app > your instance > Services > your service > Configure**, turn **Autoscaling** off, and
select **Update** before retrying the downgrade.

Disabling an app service is not enough: disabled services keep their autoscaling settings so those settings can be
restored when the service is re-enabled. You can turn autoscaling off while the service remains disabled; deleting the
service is not required. See [Application Scalability](apps/scalability.md#autoscaling-rules) for the configuration
requirements and behavior.

### Wodby CI minutes

[Wodby CI](cicd/wodby-ci.md) is the default CI system to build your applications, release artifacts, and run deployments.

Each billing cycle includes a free amount of build minutes. Additional usage is billed by total build minutes.

### Wodby registry storage

Wodby Registry is the default private Docker registry for images built and released during CI. Storage usage is billed by stored GB above the included amount.

The first 5 GB are included in each billing cycle. Wodby measures the organization's current total stored image data,
converts it to GiB, and rounds a non-whole value up to the next whole unit for billing. For example, 5.1 GiB produces a
billing quantity of 6 GiB, of which 1 GiB is above the included amount.

When the stored quantity changes, the storage charge is prorated for the portion of the billing cycle during which each
quantity applied. Deleting images can therefore reduce the remaining storage charge after the next usage
synchronization; it does not retroactively remove storage already used earlier in the cycle.

When you delete your app instance, we automatically delete all images associated with it.

You can selectively void older build images to clean up docker images while keeping the build records.

### Wodby Cloud usage

Wodby Cloud is billed in dollars as Wodby Cloud usage.

Compute usage is based on the selected machine type, node count, provisioned persistent storage, and cluster infrastructure during the billing period. Scalable Wodby Cloud clusters incur an additional cluster fee.

Paid plans include $30 of Wodby Cloud usage per month.
