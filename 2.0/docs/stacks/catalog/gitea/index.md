# Gitea

The Wodby Gitea catalog stack runs [Gitea](https://about.gitea.com/), a self-hosted Git service, with PostgreSQL and an
optional OpenSMTPD service. The current services and defaults are documented in
[`wodby/stack-gitea`](https://github.com/wodby/stack-gitea).

Gitea and PostgreSQL are required. OpenSMTPD is selected by default, and you can leave it out when you create the app.

## Administrator account

Set the administrator in the Gitea service's settings when you create the app:

| Setting | What it sets |
| --- | --- |
| Admin username | The administrator's username, `gitea_admin` by default. Some names, such as `admin`, are reserved |
| Admin password | Required. The administrator's password, at least 8 characters |
| Admin email | The administrator's email address. When empty, it is the username at the main domain |

Gitea creates this account on its first start. The web installer is never shown, so nobody else can claim the site. Open
the app's main domain and sign in with these credentials.

If the password is missing or shorter than 8 characters, Gitea stops with an error and the deployment fails. Fix the
setting and deploy again.

The settings are only used while Gitea has no administrator. Changing them later changes nothing; change the password in
Gitea.

Registration is closed. Add accounts in Gitea's **Site Administration**, or open sign-up by setting the environment
variable `GITEA__service__DISABLE_REGISTRATION` to `false` and deploying the service.

## Clone repositories

**HTTPS** works through the main domain without extra setup. Git LFS is on. The route has no request timeout, so long
clones and large pushes are not cut off.

Gitea takes its address from the main domain. After you change the main domain, Wodby marks the Gitea service for
redeployment; deploy it so that Gitea and its clone URLs use the new address.

**SSH** needs a published port. Until you publish it, SSH is off and Gitea shows only HTTPS clone URLs.

1. Open the app environment's **Endpoints > Ports** page and publish the Gitea `ssh` port. See
   [Publishing ports](../../../apps/endpoints.md#publishing-ports).
2. Wodby assigns a public port from the range `31222`-`32222` and deploys Gitea again. Gitea turns SSH on and shows SSH
   clone URLs with the main domain and that port, for example `ssh://git@gitea.example.com:31222/owner/repository.git`.
3. Add your public SSH key in Gitea under your user **Settings > SSH / GPG Keys**. Wodby SSH keys are not used for Git.

The SSH user is `git`. The cluster must support TCP port publishing; the Ports page says so if it doesn't.

## Mail delivery

The OpenSMTPD service is optional. While the Gitea app service is linked to it, Gitea sends mail through it from
`noreply@<main domain>`. To send from another address, set the `GITEA__mailer__FROM` environment variable on the Gitea
service.

Attach an [SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production delivery, and make sure
the provider accepts the sender domain. Without a relay, mail leaves directly from the cluster address, and recipient
providers often reject it. See the [OpenSMTPD guide](../opensmtpd/index.md).

Without OpenSMTPD, Gitea sends no mail.

## Change configuration

Gitea reads `GITEA__<section>__<KEY>` environment variables, for example `GITEA__service__DISABLE_REGISTRATION` for the
`DISABLE_REGISTRATION` key in the `[service]` section. On every start it writes them to its `app.ini` configuration
file. The keys are listed in Gitea's
[configuration cheat sheet](https://docs.gitea.com/administration/config-cheat-sheet/).

Add or edit the variables on the Gitea app service and deploy it. See
[Environment variables](../../../apps/environment-variables.md).

- Removing a variable does not remove its key from `app.ini`. Set the value you want instead. For example, if you remove
  the mail link from an existing app, set `GITEA__mailer__ENABLED` to `false`.
- Wodby sets the site address, the database connection, mail while the link exists, and the app's title as the site
  name. Leave these to Wodby.
- Users, organizations, and other data you manage in Gitea are kept in the database and are not affected.

Wodby generates Gitea's secret key and internal tokens and keeps them stable across deployments. They are on the Gitea
app service's **Configuration > Tokens** tab. Do not change `secret_key`: Gitea can no longer read two-factor
authentication secrets and other values it encrypted with it.

## Run CI jobs

Gitea Actions is available, but the stack includes no runner. To run workflows, register an external
[Gitea Actions runner](https://docs.gitea.com/runner/) with Gitea through the main domain.

## Data and backups

- The Gitea volume (20 GB by default) holds repositories, Git LFS objects, packages, attachments, avatars, Actions logs
  and artifacts, the SSH host keys, and `app.ini`.
- Everything else, such as users, issues, and pull requests, is in PostgreSQL, which has its own 20 GB volume.

Back up the database and the Gitea volume together as one recovery set. The Gitea service has no backup or import
operation in Wodby. The PostgreSQL service does. See [Backups](../../../apps/backups.md).

## Versions and upgrades

The Gitea service offers one version, `28`.

When a new stack revision brings a newer Gitea, upgrade the app environment's stack. See
[Upgrade](../../../apps/stack.md#upgrade). Gitea migrates its database when it starts, and Wodby waits up to 15 minutes
for it to answer. Back up first.

## Limits

- The Gitea service is fixed to one replica. Its data is on a single volume, so it can't be scaled.
- No Actions runner is included.
- Gitea requests 0.2 CPU and 512 MiB of memory and is limited to 2 CPU and 2048 MiB. Change resources under
  **Runtime > Resources**.
