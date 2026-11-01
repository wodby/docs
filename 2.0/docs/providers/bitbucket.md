# Bitbucket

After connecting your Bitbucket account you can use its repositories as a build source for applications deployed via Wodby.

Wodby completes OAuth integration creation by asking you to select a Bitbucket workspace. The selected workspace is
stored as `BITBUCKET_WORKSPACE` and determines where Wodby discovers repositories.

## Build boilerplates

Bitbucket integrations can use Bitbucket repositories as app build sources. Automated import of public build boilerplates
into new Bitbucket repositories is not supported yet.

To start from a build boilerplate with Bitbucket, create or copy the repository manually in Bitbucket, then select that
repository as the build source in Wodby.

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
