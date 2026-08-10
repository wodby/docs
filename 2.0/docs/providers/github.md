# GitHub

After connecting your GitHub account you can use your repositories as a build source for applications deployed via Wodby.

## Use one organization installation in multiple Wodby organizations

A GitHub App installation belongs to one GitHub account, so Wodby keeps one canonical integration for that
installation. If the same GitHub organization installation is already connected in another Wodby organization,
connecting it again creates an access request instead of copying the installation credentials.

Only Wodby organization owners can request, approve, decline, cancel, or revoke this access. Personal GitHub
installations cannot be shared.

The request flow is:

1. An owner in the requesting Wodby organization starts the normal GitHub integration connection and selects the
   existing GitHub organization installation.
2. Wodby verifies the installation and records the requested integration name, owner, project, and integration types.
3. Owners of the Wodby organization that holds the canonical integration review the request and approve or decline it.
4. After approval, Wodby creates a local integration in the requesting organization. It can be owned by that
   organization or by the project selected in the request and can use the normal project-sharing settings there.

Pending requests expire after seven days. An owner of the requesting organization can cancel a pending request, and
an owner of the source organization can revoke an accepted request.

To change the requested integration name, owner, project, or integration types while a request is pending, cancel the
request and start the connection again. Wodby does not change a pending request in place, so source-organization owners
always approve the settings they reviewed.

### Privacy and credential security

The requesting organization sees the GitHub provider, GitHub account scope, its requested settings, and the request
status. It does not receive the name or identifier of the Wodby organization that owns the canonical integration.
Source-organization owners see the requesting organization and requester so they can make an informed approval
decision.

Approval does not copy the GitHub App installation ID, OAuth token, or other credentials into the requesting
organization. The local integration is a credentialless handle, and Wodby checks the accepted sharing relationship
whenever it uses the canonical installation. This means revocation takes effect immediately and disables the local
integration. Existing app or CI references to that integration can no longer access GitHub until they are changed.

Deleting the local shared integration immediately revokes its access and removes only that organization's handle. It
does not uninstall the GitHub App or delete the canonical integration. Wodby prevents deletion or ownership changes of
the canonical integration while it has active shared handles; revoke those shares first.

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

- You can trigger a fresh workflow run from Wodby without a previous build
- Link the app service to the GitHub repository and configure a branch or tag plus the workflow file name or numeric ID
- You can also re-run the workflow run associated with the last recorded build
- The GitHub App installation must have access to the repository with Actions permissions enabled
- Starting a new workflow run requires the workflow to support `workflow_dispatch`
