# Email notifications

Choose which optional emails you receive from Wodby under `Account > Notifications`.
Settings are kept separately for each organization and apply only to your
account: other members of the organization are not affected.

## Optional emails

Every optional email is on until you turn it off.

| Email | When it is sent | Who receives it |
| --- | --- | --- |
| Application deployed | An application you created finishes its first deployment. | You |
| Server connected | A server you connected is ready for application deployments. | You |
| Failed automatic backups | Daily, when an enabled automatic backup has missed its schedule. See [Failure reports](../apps/backups.md#failure-reports). | Organization owners and administrators |
| Weekly organization report | Weekly summary of servers, applications, updates, access, and security. | Organization owners and administrators |

An "Application deployed" email that contains generated administrator
credentials is always sent, because it is the only copy of those credentials.

Turning an email off does not affect the alerts shown in the dashboard.

The following emails are always sent and cannot be turned off: account and
security emails, organization invitations, legal notices, and billing emails.

## Change your settings

1. Open `Account > Notifications`.
2. Select the **Organization**.
3. Select or clear the checkbox next to each email. Changes are saved
   immediately.

To turn every optional email off for the selected organization, click
**Unsubscribe from all** and confirm. To turn them all back on, click
**Subscribe to all**.

You can change settings for any organization you belong to. A setting you
choose before becoming an owner or administrator applies once you receive that
role.

## Unsubscribe from an email

The weekly organization report includes an unsubscribe link. Other optional
emails link to your notification settings.

1. Click the unsubscribe link in the email.
2. Review the email type and organization on the page that opens.
3. Click **Unsubscribe**.

The link turns off only that email, only for that organization. Opening the
link without clicking **Unsubscribe** changes nothing.

If your email client shows its own unsubscribe button for the weekly report,
such as in Gmail, it unsubscribes you without the confirmation page.

Unsubscribe links expire 14 days after the email is sent. If a link has expired,
or you turned the email back on after using it, change the setting under
`Account > Notifications` instead.
