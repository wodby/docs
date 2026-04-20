# GitHub

After connecting your GitHub account you can use your repositories as a build source for applications deployed via Wodby or to clone existing public build templates.

## Actions

Wodby supports GitHub Actions as a third-party CI integration.

- You can trigger a new build from Wodby by starting a new workflow run based on the last recorded build
- You can also re-run the workflow run associated with the last recorded build
- The GitHub App installation must have access to the repository with Actions permissions enabled
- Starting a new workflow run requires the workflow to support `workflow_dispatch`
