---
description: Connect Bitbucket to Wodby to build applications from your repositories, with build boilerplates and preview environments for pull requests.
---

# Bitbucket

After connecting your Bitbucket account you can use its repositories as a build source for applications deployed via Wodby.

Wodby completes OAuth integration creation by asking you to select a Bitbucket workspace. The selected workspace is
stored as `BITBUCKET_WORKSPACE` and determines where Wodby discovers repositories.

## Build boilerplates

Wodby can't create repositories on Bitbucket, so you create the repository first. Wodby copies the boilerplate into it
at the app's first deployment.

1. In the integration's workspace on Bitbucket, create an empty repository, without a README or `.gitignore`.
2. In Wodby, choose **Clone boilerplate**, select the Bitbucket integration, and enter the repository's name as it
   appears in its URL. Names can use letters, digits, dots, dashes, and underscores.

If the repository doesn't exist or already has commits, Wodby stops before creating the app and tells you what to fix.

The connected Bitbucket account needs write access to the repository; without it, the app is created but its first
deployment fails. For pushes to start builds, the account also needs the **Admin** permission on the repository. Without
it, the deployment continues and its log warns you. If you connected the integration before Wodby supported Bitbucket
webhooks, reconnect it once.

Wodby builds from the boilerplate's branch. If the repository's main branch is a different one, the deployment continues
and its log warns you. You can change the main branch in the repository settings on Bitbucket.

To build from a repository that already has code, select it as the build source instead.

## Preview environments

Bitbucket integrations can create [preview environments](../apps/preview-environments.md) for pull requests.

- The integration's Bitbucket account needs the `Admin` permission on the repository. Wodby needs it to add its webhook
  and to check who gave a command, because Bitbucket shows permissions only to admins.
- If Wodby cannot add the webhook, the task shows a warning and Wodby retries every hour. Until the webhook exists, pushes
  do not start builds or rebuild previews, and `/wodby` commands get no answer. Previews are still created and deleted
  by the check that runs every 15 minutes. To fix it, reconnect the integration with an account that has the `Admin`
  permission.
- Wodby reacts to pull requests that target the branch followed by the app's base environment. Pull requests from forks
  are ignored.
- Each deployment is reported as a `wodby/preview` build status on the commit it built, and Wodby keeps one comment on
  the pull request up to date with the preview's state and URL.
- People with write or admin access to the repository can comment `/wodby preview` or `/wodby reseed` on the pull
  request. Bitbucket has no comment reactions, so Wodby explains a refused command in its comment. See
  [Pull request commands](../apps/preview-environments.md#pull-request-commands).
