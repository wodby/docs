# GitLab

The Wodby GitLab catalog stack runs GitLab Community Edition 19 from the official GitLab Helm chart, with PostgreSQL 17,
Valkey 8.1, OpenSMTPD, and an optional GitLab Runner. The current composition is documented in
[`wodby/stack-gitlab`](https://github.com/wodby/stack-gitlab).

GitLab, PostgreSQL, Valkey, and OpenSMTPD are required. The GitLab Runner service is disabled until you enable it.

## Before you create the app

- Prepare S3-compatible object storage and a variable integration for it, as described below. GitLab can't be created
  without it.
- Plan capacity. GitLab names 16 GB of memory and 8 vCPU as the baseline for a single-node installation. The cluster
  must fit GitLab's web, background job, Git, SSH, Registry, and toolbox pods together with PostgreSQL, which requests
  0.5 CPU and 2.5 GiB of memory, with limits of 2 CPU and 4 GiB. CI jobs add their own pods. See the
  [GitLab installation requirements](https://docs.gitlab.com/install/requirements/).
- Set up a custom domain as the main domain if you want GitLab, its clone URLs, and its mail to use your own hostname.
  See [Endpoints](../../../apps/endpoints.md#custom-domains-and-redirects).

## Prepare object storage

GitLab keeps CI artifacts, Git LFS objects, uploads, packages, Container Registry images, and backup archives in object
storage. Create seven buckets with distinct names before you create the app: artifacts, LFS, uploads, packages,
Registry, backups, and temporary restore data. GitLab serves artifact, LFS, upload, and package downloads itself.

The GitLab app service requires an **S3-compatible object storage** integration that supplies these variables:

| Variable | Secret | Value |
| --- | --- | --- |
| `GITLAB_OBJECT_STORAGE_CONNECTION` | Yes | GitLab's object storage connection in YAML, such as provider, region, keys, and endpoint |
| `GITLAB_REGISTRY_STORAGE_CONFIG` | Yes | The contents of the Registry `storage` block, with an S3 driver and the Registry bucket |
| `GITLAB_BACKUP_S3_CONFIG` | Yes | An `s3cmd` configuration file for the backup tool |
| `GITLAB_ARTIFACTS_BUCKET` | No | Bucket for CI artifacts |
| `GITLAB_LFS_BUCKET` | No | Bucket for Git LFS objects |
| `GITLAB_UPLOADS_BUCKET` | No | Bucket for uploads |
| `GITLAB_PACKAGES_BUCKET` | No | Bucket for packages |
| `GITLAB_REGISTRY_BUCKET` | No | Bucket for Container Registry images, the same one named in the Registry configuration |
| `GITLAB_BACKUPS_BUCKET` | No | Bucket for backup archives |
| `GITLAB_BACKUPS_TMP_BUCKET` | No | Bucket for temporary restore data |

The formats are described in GitLab's
[external object storage](https://docs.gitlab.com/charts/advanced/external-object-storage/) guide.

To supply the variables, create a [custom variable provider](../../../providers/custom-variable-providers.md) with
`New from manifest`, create an integration from it with your values, and select that integration for GitLab when you
create the app. Secret variables must come from secret fields. For example:

```yaml
name: gitlab-object-storage
title: GitLab object storage
icon: variable

kinds:
  - name: s3
    title: S3-compatible object storage for GitLab
    type: variable
    fields:
      - type: textarea_upload
        secret: true
        name: connection
        label: Object storage connection
        variable: GITLAB_OBJECT_STORAGE_CONNECTION
      - type: textarea_upload
        secret: true
        name: registry_storage
        label: Registry storage configuration
        variable: GITLAB_REGISTRY_STORAGE_CONFIG
      - type: textarea_upload
        secret: true
        name: backup_s3cfg
        label: Backup s3cmd configuration
        variable: GITLAB_BACKUP_S3_CONFIG
      - type: text
        name: artifacts_bucket
        label: Artifacts bucket
        variable: GITLAB_ARTIFACTS_BUCKET
      - type: text
        name: lfs_bucket
        label: LFS bucket
        variable: GITLAB_LFS_BUCKET
      - type: text
        name: uploads_bucket
        label: Uploads bucket
        variable: GITLAB_UPLOADS_BUCKET
      - type: text
        name: packages_bucket
        label: Packages bucket
        variable: GITLAB_PACKAGES_BUCKET
      - type: text
        name: registry_bucket
        label: Registry bucket
        variable: GITLAB_REGISTRY_BUCKET
      - type: text
        name: backups_bucket
        label: Backups bucket
        variable: GITLAB_BACKUPS_BUCKET
      - type: text
        name: backups_tmp_bucket
        label: Temporary restore bucket
        variable: GITLAB_BACKUPS_TMP_BUCKET
```

See [Variable integration](../../../integrations/variable.md) for how integrations are attached.

## First sign-in

Wodby generates the password of GitLab's `root` administrator when the app is created.

1. Open the GitLab app service's **Configuration > Tokens** tab and reveal `root_password`. See
   [Tokens](../../../apps/tokens.md).
2. Open the app's main domain and sign in as `root` with that password.
3. Change the password in your user settings.

GitLab uses the token only when it creates its database during the first deployment. Changing the token later does not
change the password.

By default, anyone who can open GitLab can register an account, and an administrator must approve each new account.
Review this under **Admin area > Settings > General > New user account restrictions**.

GitLab takes its address from the main domain when it is deployed. After you change the main domain, deploy the app
environment so GitLab, its clone URLs, and the runner use the new address.

## Clone repositories

**HTTPS** works through the main domain without extra setup. GitLab shows the clone URL on each project page.

**SSH** needs a published port. GitLab's SSH endpoint isn't reachable from outside the cluster until you publish it:

1. Open the app environment's **Endpoints > Ports** page and publish the GitLab `ssh` port. See
   [Publishing ports](../../../apps/endpoints.md#publishing-ports).
2. Wodby assigns a public port from the range `31222`-`32222` and deploys GitLab again, so that GitLab's SSH clone URLs
   show the main domain with that port, for example `ssh://git@gitlab.example.com:31222/group/project.git`.
3. Add your public SSH key to your GitLab user settings. Wodby SSH keys are not used for Git.

Before the port is published, GitLab shows SSH clone URLs on port `22`, which don't work. The cluster must support TCP
port publishing; the Ports page says so if it doesn't.

## Container Registry

The Container Registry has its own public domain, separate from the main domain. Each project's container registry page
in GitLab shows the registry address and the `docker login`, build, and push commands.

The Registry domain has a 15-minute request timeout. If pushing a large image layer takes longer, raise
`request_timeout` and `backend_request_timeout` for that domain. See
[HTTP settings](../../../apps/endpoints.md#http-settings).

## Run CI jobs

The **GitLab Runner** service is disabled by default. To enable it:

1. In GitLab, create a runner and copy its authentication token, which begins with `glrt-`. Registration tokens are not
   supported.
2. On the Runner app service, set **Runner authentication token** to that token. See
   [Settings tab](../../../apps/services.md#settings-tab).
3. Enable the Runner app service and deploy it.

The runner connects to GitLab through the main domain. Configure tags, protected-branch access, and whether untagged
jobs run on the runner in GitLab.

How jobs run:

- Each job runs in its own pod, in the same Kubernetes namespace as GitLab. Up to four jobs run at once.
- Jobs without an `image` use `alpine:3.22`.
- A job container requests 0.1 CPU and 256 MiB of memory, with limits of 2 CPU and 2 GiB. A job cannot raise these
  limits.
- Job containers are unprivileged, so Docker-in-Docker is not available. Build container images with a builder that
  doesn't need privileged mode.
- No distributed cache is configured, so CI `cache` entries are not kept between jobs. Artifacts are kept in object
  storage.

## Mail delivery

GitLab sends mail through the stack's OpenSMTPD service, from `gitlab@<main domain>` with a reply-to address of
`noreply@<main domain>`. Attach an [SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for reliable
delivery, and make sure the provider accepts that sender domain. Without a relay, mail leaves directly from the cluster
address, and recipient providers often reject it. See the [OpenSMTPD guide](../opensmtpd/index.md).

To send from another address, override the GitLab chart value `global.email.from` on the GitLab app service's
**Configuration > Helm** tab and deploy it. See [Helm tab](../../../apps/services.md#helm-tab).

Incoming email, such as replying to notifications by email, is disabled.

## Data and backups

- Git repositories and wikis are on the GitLab `repositories` volume (50 GB by default).
- Database data is on the PostgreSQL volume (20 GB by default).
- Valkey keeps its data on a 10 GB volume with persistence on. It can use up to 1 GB of memory and never removes keys
  to free memory, because it holds GitLab's background jobs and sessions.
- Artifacts, LFS objects, uploads, packages, and Registry images are in your object storage.

GitLab creates a backup archive every day at 01:00 in the cluster's time zone and uploads it to the backups bucket. The
archive contains the database, repositories and wikis, Registry images, and the object storage data. Runs don't overlap
and are stopped after six hours. Each run uses a temporary 100 GiB volume, so the cluster must be able to provision one.

These archives are not Wodby backups. They don't appear on the app environment's **Backups** page, and Wodby doesn't
remove old ones. Set retention and replication on the backups bucket.

GitLab leaves its Rails secrets out of the archive. A restore needs them, so keep a separately protected copy. See
GitLab's [Back up the secrets](https://docs.gitlab.com/charts/backup-restore/backup/#back-up-the-secrets).

The PostgreSQL service also has a Wodby database backup and import. Use them as an extra layer for the database only.
They don't contain repositories or object storage data, so they can't restore GitLab on their own. See
[Backups](../../../apps/backups.md) and [Imports](../../../apps/imports.md).

## Restore or move GitLab

To restore an archive, or to move an existing GitLab installation into this stack, follow GitLab's
[Helm restore procedure](https://docs.gitlab.com/charts/backup-restore/restore/). The archive must come from the same
GitLab version, the Rails secrets must be restored too, and GitLab's web and background job pods must be stopped while
the restore runs.

## Upgrades

Upgrade GitLab by [upgrading the app environment's stack](../../../apps/stack.md#upgrade) when a new revision changes
the GitLab version. GitLab must pass its [required upgrade stops](https://docs.gitlab.com/update/upgrade_paths/). Before
each upgrade, check that background migrations have finished in the Admin area and take a backup you have tested.

New non-production environments upgrade their stack automatically by default. Turn
[auto-upgrade](../../../apps/stack.md#auto-upgrade) off for GitLab environments whose upgrades you want to control.

## Limits

- GitLab runs as a single instance and is not scalable. For high availability, see GitLab's
  [Cloud Native Hybrid](https://docs.gitlab.com/administration/reference_architectures/cloud_native/) guidance.
- GitLab Pages, the GitLab agent for Kubernetes server, incoming email, and the bundled monitoring are disabled.
- Terraform state, CI/CD secure files, and the dependency proxy are not enabled.
