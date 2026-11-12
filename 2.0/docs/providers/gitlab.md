---
description: Connect GitLab to Wodby to build applications from your repositories, with build boilerplates, GitLab CI and preview environments.
---

# GitLab

After connecting your GitLab account you can use your repositories as a build source for applications deployed via Wodby.

## Build boilerplates

GitLab integrations can use GitLab repositories as app build sources. When a service provides a public build
boilerplate, Wodby can create a new GitLab repository and import the boilerplate contents into it during new app
creation.

The target repository is created in the selected GitLab integration namespace:

- If the integration has a scope, Wodby uses that scope as the user, group, or subgroup path.
- If the integration has no scope, Wodby uses the authenticated GitLab user's namespace.

The GitLab user or token actor must be allowed to create projects in that namespace.

## Auth

Wodby supports two authentication methods for GitLab:

- OAuth2 for GitLab.com
- Token authentication for GitLab.com and self-hosted GitLab

When using token authentication:

- You can use a personal, group, or project access token
- Required scopes for Git repository access: `read_api` and `read_repository`
- Use `api` instead of `read_api` if you plan to clone build boilerplates into new repositories, use GitLab CI features such as re-running jobs, or create new pipelines
- Required role: `Developer` or higher for both Git and CI integrations
- To clone build boilerplates, the token actor must be allowed to create projects in the target namespace
- For self-hosted GitLab, specify the GitLab base URL. Leave it empty for GitLab.com
- A self-hosted GitLab must be reachable from the public internet. Wodby can't connect to private or internal addresses,
  so an instance available only on a private network or VPN can't be used
- To change the base URL of an existing integration, enter the access token again
- If you want to run GitLab CI builds from Wodby, make sure the token's actor is allowed to run pipelines for protected branches such as `main`

Token authentication asks for:

| Field | Required | Description |
| --- | --- | --- |
| GitLab Base URL | No | Base URL of a self-hosted GitLab installation, reachable from the public internet. Leave empty for GitLab.com. |
| GitLab access token | Yes | Personal, group, or project access token with the scopes and role described above. |

## CI

Wodby supports GitLab CI as a third-party CI integration.

- You can trigger a fresh pipeline from Wodby without a previous build
- Link the app service to the GitLab repository and configure the branch or tag used for new pipelines
- You can re-run the last recorded build by retrying the associated GitLab job
- Self-hosted GitLab is supported via token authentication

## Preview environments

GitLab integrations can create [preview environments](../apps/preview-environments.md) for merge requests.

- The connected account or token needs the `Maintainer` role on the project, and an access token needs the `api` scope.
  This is more than a build source needs: Wodby adds its webhook to the project and writes statuses and comments on merge
  requests.
- If Wodby cannot add the webhook, the task shows a warning and Wodby retries every hour. Until the webhook exists, pushes
  do not start builds or rebuild previews, and `/wodby` commands get no answer. Previews are still created and deleted
  by the check that runs every 15 minutes.
- Wodby reacts to merge requests that target the branch followed by the app's base environment. Merge requests from forks
  are ignored.
- Each deployment is reported as a `wodby/preview` commit status on the commit it built, and Wodby keeps one comment
  on the merge request up to date with the preview's state and URL.
- Project members with the `Developer` role or higher can comment `/wodby preview` or `/wodby reseed` on the merge
  request. See [Pull request commands](../apps/preview-environments.md#pull-request-commands).
