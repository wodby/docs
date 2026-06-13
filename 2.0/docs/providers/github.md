# GitHub

After connecting your GitHub account you can use your repositories as a build source for applications deployed via Wodby.

## Build template import

GitHub integrations support importing public build templates into new GitHub repositories during app creation.

When a service provides a public build template, Wodby can create a new repository in the selected GitHub
user or organization account and mirror the template contents into it. Use this when you want to start from template
code but own the resulting repository.

- The selected GitHub connection must be allowed to create and write to the target repository
- Wodby uses the GitHub App installation to access organization repositories when applicable
- Wodby uses the connected GitHub OAuth token when creating user-owned repositories and when mirroring template contents

## Actions

Wodby supports GitHub Actions as a third-party CI integration.

- You can trigger a new build from Wodby by starting a new workflow run based on the last recorded build
- You can also re-run the workflow run associated with the last recorded build
- The GitHub App installation must have access to the repository with Actions permissions enabled
- Starting a new workflow run requires the workflow to support `workflow_dispatch`
