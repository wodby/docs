# GitLab

After connecting your GitLab account you can use your repositories as a build source for applications deployed via Wodby.

## Build templates

GitLab integrations can use GitLab repositories as app build sources. When a service provides a public build
template, Wodby can create a new GitLab repository and import the template contents into it during new app creation.

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
- Use `api` instead of `read_api` if you plan to clone build templates into new repositories, use GitLab CI features such as re-running jobs, or create new pipelines
- Required role: `Developer` or higher for both Git and CI integrations
- To clone build templates, the token actor must be allowed to create projects in the target namespace
- For self-hosted GitLab, specify the GitLab base URL. Leave it empty for GitLab.com
- If you want to run GitLab CI builds from Wodby, make sure the token's actor is allowed to run pipelines for protected branches such as `main`

## CI

Wodby supports GitLab CI as a third-party CI integration.

- You can trigger a new build from Wodby by creating a new pipeline for the same ref as the last recorded build
- You can re-run the last recorded build by retrying the associated GitLab job
- Self-hosted GitLab is supported via token authentication
