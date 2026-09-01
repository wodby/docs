# Notifications

Manage email notification preferences from `User settings > Notifications`.

Notification settings are personal to your Wodby user. They are also scoped to one organization at a time.

## Choosing an organization

Use the organization selector at the top of the page to choose which organization's email notifications you want to configure.

Changing a notification setting affects only:

- your user account
- the selected organization
- the specific notification type you changed

It does not change notification delivery for other organization members.

## What you can configure

The page groups notification types by category, such as apps, clusters, automation, integrations, billing, and reports.

Each notification has its own toggle. Turning a notification off stops that type of email for your user in the selected organization.

Examples include:

- failed app builds or deployments
- app creation results
- cluster creation or connection events
- successful or failed automatic cluster infrastructure upgrades
- automatic service source updates, inherited-service base revision updates, Git-backed stack updates, stack service
  revision updates, origin stack syncs, and app stack upgrades
- cron job and backup failures and recoveries, plus failed imports, certificate renewals, custom certificate expiration, service actions, or integration installs
- breached spending limits
- weekly organization reports

## Scheduled cron and backup notifications

The `Cron job failures and recoveries` and `Backup failures and recoveries` settings control both failure and recovery
emails for scheduled automation. Wodby emails organization admins when a schedule's latest conclusive result first
changes to failed. Repeated failures are suppressed while that schedule remains in the failed state. The first later
conclusive success sends a recovery email.

An automatic backup preset can create several backup artifacts in one scheduled occurrence. Any failed artifact makes
the occurrence fail, but recovery is reported only after every artifact in a later occurrence completes successfully.

A failed manual cron job or backup still emails the user who started it.

## Custom certificate expiration notifications

The `Custom certificate expiration` setting controls warnings for uploaded TLS certificates, which Wodby does not
renew automatically. Wodby emails organization admins 30, 14, 7, and 1 day before expiration and once after the
certificate expires. Each stage is sent once for a certificate's current expiration date.

## Weekly organization report

The weekly organization report includes an `Automation health` section with enabled cron schedules and automatic
backup presets whose latest conclusive result is still failed. This keeps ongoing failures visible while repeated
immediate failure emails are suppressed.

## Defaults

Notifications are enabled by default unless you turn them off.

If you have not saved a preference for a notification type yet, Wodby treats it as enabled.

## Access

Notification settings are available to users who can view the selected organization. The settings are the same regardless of your organization role because they control your own email preferences, not organization-wide behavior.

## Email unsubscribe links

Unsubscribe links in notification emails update the same personal, organization-scoped setting shown on this page.

## Related pages

- [User settings](index.md)
- [Emails](emails.md)
- [Organization](../org.md)
