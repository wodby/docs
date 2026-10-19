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
emails for scheduled automation:

- **Cron jobs:** Wodby emails organization admins on the first failure, then at most once every 24 hours when further
  runs fail. Repeated-failure emails use **Scheduled cron job still failing**. A new failure after a successful run
  sends an immediate email.
- **Backups:** Each failed scheduled occurrence sends an email. Repeated-failure emails use
  **Scheduled backup still failing**.
- **Recovery:** The first later conclusive success sends a recovery email immediately.

Cron and backup execution schedules stay as configured. Failure logs and emails include the next scheduled attempt
when available; disabled or overdue schedules are identified separately. If you change the schedule afterward, the
next run can differ from the time in an earlier message.

An automatic backup preset can create several backup artifacts in one scheduled occurrence. Any failed artifact makes
the occurrence fail, but recovery is reported only after every artifact in a later occurrence completes successfully.

A failed manual cron job or backup still emails the user who started it.

## Certificate renewal notifications

For automatic Let's Encrypt renewal, Wodby notifies organization admins after every failed attempt. The first email
uses **Certificate renewal failed**; later failures use **Certificate renewal still failing**.

Retry delays increase with consecutive failures: **1 day, 2 days, 3 days, 4 days, 5 days, 6 days, then 7 days** between
attempts. Further retries stay seven days apart. A small offset spreads attempts across certificates, and a longer
certificate-authority retry delay takes precedence. Successful renewal resets the failure history.

If a certificate expires before the next retry, Wodby schedules one additional renewal attempt at expiry, or when the
app and cluster next become eligible. A later retry time required by the certificate authority still takes precedence.
After this attempt, the ordinary backoff resumes.

If the certificate is already expired when a failure email is prepared, its subject says
**Certificate expired; renewal failed**. The Cloudflare action suffix remains when that attempt confirmed a browser
challenge. Emails covering both expired and valid certificates explicitly identify that the batch includes expired
certificates.

Failure task logs and emails include the next scheduled retry time. The relative delay is measured when the message
is generated; it is not a countdown that updates in your inbox. Correct external validation problems before expiry,
using the troubleshooting links below.

The first successful automatic retry after previous failures sends a **Certificate renewal recovered** email. The
certificate renewal notification preference controls both failure and recovery emails. If a task renews several
certificates, recovery is reported for the certificates that recovered, even if others still failed.

If a notification identifies a Cloudflare browser challenge, follow the
[Cloudflare troubleshooting steps](../providers/cloudflare.md#certificate-validation-behind-cloudflare). See
[certificate troubleshooting](../apps/certificate-troubleshooting.md) for other validation errors.

## Custom certificate expiration notifications

The `Custom certificate expiration` setting controls warnings for uploaded TLS certificates, which Wodby does not
renew automatically. Wodby emails organization admins 30, 14, 7, and 1 day before expiration and once after the
certificate expires. Each stage is sent once for a certificate's current expiration date.

## Weekly organization report

The weekly organization report includes an `Automation health` section with enabled cron schedules and automatic
backup presets whose latest conclusive result is still failed. It also shows ongoing issues when a cron schedule has
not produced another run eligible for a reminder.

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
