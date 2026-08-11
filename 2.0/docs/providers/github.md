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

- Link the app service to the GitHub repository and run the first workflow outside Wodby so its workflow ID and ref can
  be recorded
- After a workflow has been recorded, you can trigger a fresh workflow run from Wodby
- You can also re-run the workflow run associated with the last recorded build
- The GitHub App installation must have access to the repository with Actions permissions enabled
- Starting a new workflow run requires the workflow to support `workflow_dispatch`
