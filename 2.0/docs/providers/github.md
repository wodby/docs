# GitHub

After connecting your GitHub account you can use your repositories as a build source for applications deployed via Wodby.

## Use one organization installation in multiple Wodby organizations

A GitHub App installation can be connected to Wodby only once. If another Wodby organization needs the same
installation, do not start the GitHub connection flow again: GitHub will show only `Configure` for an existing
installation and does not send a new installation result to Wodby.

Instead, an owner of the Wodby organization that already holds the GitHub integration opens its `Sharing` page and
invites the other Wodby organization by its exact machine name. An owner of the invited organization then reviews the
request under `Integrations > OAuth invitations` and chooses the local integration name and title.

Wodby keeps the GitHub App installation and OAuth credentials only on the canonical integration. The accepted
organization receives a credentialless local handle, and source owners can revoke it at any time. See
[Share an OAuth integration with another organization](../integrations/organization-sharing.md) for the complete
owner, privacy, expiration, and revocation rules.

## Build boilerplate import

GitHub integrations support importing public build boilerplates into new GitHub repositories during app creation.

When a service provides a public build boilerplate, Wodby can create a new repository in the selected GitHub
user or organization account and mirror the boilerplate contents into it. Use this when you want to start from
boilerplate code but own the resulting repository.

- The selected GitHub connection must be allowed to create and write to the target repository
- Wodby uses the GitHub App installation to access organization repositories when applicable
- Wodby uses the connected GitHub OAuth token when creating user-owned repositories and when mirroring boilerplate contents

## Actions

Wodby supports GitHub Actions as a third-party CI integration.

- Link the app service to the GitHub repository, select a branch or tag, and run the first workflow on that ref outside
  Wodby so its workflow ID can be recorded
- After a matching workflow has been recorded, you can trigger a fresh workflow run from Wodby on the selected ref
- You can also re-run the workflow run associated with the last recorded build
- The GitHub App installation must have access to the repository with Actions permissions enabled
- Starting a new workflow run requires the workflow to support `workflow_dispatch`

## Preview environments

GitHub integrations can create [preview environments](../apps/preview-environments.md) for pull requests.

- The GitHub App installation must be allowed to read pull requests, create commit statuses, comment on pull
  requests, and read and react to issue comments. GitHub asks the installation owner to approve these permissions when
  they are missing. Until they are approved, Wodby still creates previews but cannot report their status to the pull
  request, and pull request commands are ignored.
- Wodby reacts to pull requests that target the branch followed by the app's base environment. Pull requests from forks
  are ignored.
- Each deployment is reported as a `wodby/preview` commit status on the commit it built, and Wodby keeps one comment
  on the pull request up to date with the preview's state and URL.
- People with write access to the repository can comment `/wodby preview` or `/wodby reseed` on the pull request. See
  [Pull request commands](../apps/preview-environments.md#pull-request-commands).
