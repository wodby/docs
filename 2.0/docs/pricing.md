# Billing

## Plans

Live pricing is available at https://wodby.com/pricing.

Wodby has three plans.

### Developer

Free subscription designed for evaluation and development work.

Typical included capabilities:

- 10 app services
- 30 minutes of Wodby CI per month
- 5 GB of private container registry storage
- 5M free [AI credits](#ai-credits) tokens for Wodby Agent, granted once
- logs streaming
- stacks updates
- unlimited projects
- manual backups and imports
- technical domains with SSL
- community support

### Team

Designed for small teams and production workloads. Limits can be increased with addons.

Team includes everything in Developer, plus production-focused features such as:

- custom domains
- auto-renewed SSL certificates
- uploaded custom TLS certificates
- autoscaling tools
- app environment pausing
- backup presets and automatic backups
- scheduled and manually run cron jobs
- web shell for containers
- Application Access for protected or private-network HTTP endpoints
- organization Single Sign-On (SSO)
- best-effort support
- $30 of Wodby Cloud usage per month
- 10M free [AI credits](#ai-credits) tokens in total for Wodby Agent, granted once

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
- AI credits you buy, and additional AI credits usage on paid plans
- Infrastructure costs from your cloud provider if you use managed Kubernetes, managed databases, or other resources in your own account

Organization users and projects are included in your plan and are not billed separately. Projects have no plan-based
quantity limit.

## Addons

Addons let you extend included limits and pay for extra usage when needed.

- Addons have some free number of units every billing cycle
- Addons are pay-as-you-go, and billing is calculated at the end of the cycle
- You are charged only for usage above the free included amount
- Free subscription is not eligible for exceeding addon limits
- Organization owners on paid subscriptions can use optional spending limits for the main plan and for individual addons in the billing settings

## Spending limits

From `Organization > Billing > Usage`, organization owners on paid subscriptions can set optional spending limits for:

- the main app-service plan usage
- individual addons such as Wodby CI minutes, registry storage, Wodby Blob Storage, and Wodby Cloud usage
- additional [AI credits](#ai-credits) usage

In practice:

- leaving the value empty means `Unlimited`, except for AI credits, where additional usage is off until you set a limit
- the main plan limit cannot be set below the included app-service amount for that plan
- addon limits are configured separately per addon
- operations that would exceed a limit can be blocked, and the billing UI shows that the limit was exceeded

Only organization owners can change subscription settings, open the customer portal, downgrade, upgrade, update spending limits, manage payment methods, or buy AI credits. Other roles with billing visibility have read-only access.

On the free plan, usage above included addon amounts is not allowed. In that case you must either upgrade or wait for the next billing cycle when the addon is renewable.

## Payment methods

Organization owners manage the organization's cards in `Organization > Billing > Payment methods`. Card details go
directly to Stripe, Wodby's payment processor.

- Select **Add card** to save a card. The first card you add becomes the default.
- The default card pays subscription invoices and is preselected when you buy AI credits. Select **Make default** to
  use another card. The card you pay with when you upgrade is saved here as the default.
- On a paid plan, you can't remove the default card. Make another card the default first.
- Cards stay saved after a downgrade, so you can keep buying AI credits on the Developer plan.

Invoices are in the Stripe customer portal.

## Downgrading a paid subscription

When you downgrade a paid subscription, the downgrade is scheduled for the end of the current billing cycle. The existing paid billing period continues for billing and existing resource usage until the current period ends, and the organization moves to the free Developer plan after that.

Usage-based charges can still accrue until the end of the billing cycle. The final invoice can include addon usage and Wodby Cloud usage above the included amounts for the period.

After a downgrade is scheduled:

- you can continue using existing resources until the billing period ends
- usage-based addons can continue to accrue charges until the period ends
- organization owners can still update spending limits
- new paid-only features and capacity above the Developer plan limit are not available

To schedule a downgrade, the organization must already fit the Developer plan limits and must not depend on paid-only
features. Application Access is a paid feature, so remove it from every app environment under **Apps > your app > your
environment > Settings > Access** before scheduling a downgrade. The downgrade error identifies each affected app and
environment.

App environment pausing is also a paid feature, so no environment can be `Pausing` or `Paused` when a downgrade is
scheduled. If an environment is `Pausing`, wait for it to reach `Paused`; then open **Apps > your app > your environment >
Settings > Pause & Resume**, select **Resume app environment**, and retry the downgrade after it finishes. The downgrade
error identifies each affected app and environment.

Uploaded custom TLS certificates are also paid-only organization resources. Detach them from every route and delete
them from **Organization > Certificates** before scheduling a downgrade. An uploaded certificate blocks downgrade even
when it is currently unused because it remains stored for later reuse.

If autoscaling is configured, the downgrade error identifies the affected app, environment, and service. Open each
service from **Apps > your app > your environment > Stack > App services > your service > Configuration > General**, turn
**Autoscaling** off, and select **Update** before retrying the downgrade.

Disabling an app service is not enough: disabled services keep their autoscaling settings so those settings can be
restored when the service is re-enabled. You can turn autoscaling off while the service remains disabled; deleting the
service is not required. See [Application Scalability](apps/scalability.md#autoscaling-rules) for the configuration
requirements and behavior.

Organization SSO is also a paid feature. Disable every provider from **Organization > SSO** before scheduling a
downgrade. Provider configuration and verified domains can remain in the organization while it uses the Developer
plan, but the providers cannot be enabled or used for sign-in until the organization upgrades again.

### Wodby CI minutes

[Wodby CI](cicd/wodby-ci.md) is the default CI system to build your applications, push artifacts, and run deployments.

Each billing cycle includes a free amount of build minutes. Additional usage is billed by total build minutes.

### Wodby registry storage

Wodby Registry is the default private container registry for images built and pushed during CI. Storage usage is billed by stored GB above the included amount. It costs $0.15 per stored GB.

The first 5 GB are included in each billing cycle. Wodby measures the organization's current total stored image data,
converts it to GiB, and rounds a non-whole value up to the next whole unit for billing. For example, 5.1 GiB produces a
billing quantity of 6 GiB, of which 1 GiB is above the included amount.

When the stored quantity changes, the storage charge is prorated for the portion of the billing cycle during which each
quantity applied. Deleting images can therefore reduce the remaining storage charge after the next usage
synchronization; it does not retroactively remove storage already used earlier in the cycle.

When you delete your app environment, we automatically delete all images associated with it.

You can selectively void older build images to clean up docker images while keeping the build records.

### Wodby Blob Storage

[Wodby Blob Storage](providers/wodby-blob-storage.md) is the built-in destination for backup archives. It costs $0.05
per stored GB and has no included free storage. Data transfer is not billed.

Usage reflects the organization's current completed backup data stored by Wodby. Removing backup objects reduces the
quantity after cleanup and the next usage synchronization; it does not retroactively remove storage billed earlier in
the cycle.

### Wodby Cloud usage

Wodby Cloud is billed in dollars as Wodby Cloud usage.

Compute usage is based on the selected machine type, node count, provisioned persistent storage, and cluster infrastructure during the billing period. Scalable Wodby Cloud clusters incur an additional cluster fee.

Paid plans include $30 of Wodby Cloud usage per month.

### AI credits

AI credits pay for [Wodby Agent](apps/wodby-agent.md) and for opencode in
[development workspaces](apps/workspaces.md#connect-your-editor-or-agent) when it uses the default GLM 5.3 model.
Usage is counted in tokens, and every input, cached input and output token counts the same. Tokens cost $1.00 per 1M.

- **Free tokens**: your organization gets 5M tokens once on the Developer plan. The first time it subscribes to a
  paid plan, the total rises to 10M. Free tokens don't renew.
- **Purchased tokens**: select **Buy tokens** on the **AI credits** card in `Organization > Billing > Usage`, enter
  whole millions (1M to 10,000M) and pay with a saved [payment method](#payment-methods). If your bank asks you to
  confirm the payment, confirm it in the dialog. Purchased tokens never expire and are used after the free tokens,
  on any plan.
- **Additional usage**: on paid plans, usage beyond the free and purchased tokens is billed with your subscription
  at $1.00 per 1M tokens. It's off until an owner sets a spending limit in dollars on the AI credits card, and it
  stops at that limit or when a downgrade is scheduled.

On the Developer plan, Wodby Agent stops when the free and purchased tokens run out. Buy tokens or upgrade.

A refund or dispute of a purchase removes its tokens. If they were already used, the purchased balance becomes
negative and Wodby Agent stops until you buy enough tokens to cover it or the dispute is resolved in your favor.
