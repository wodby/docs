# GitLab

After connecting your GitLab account you can use your repositories as a build source for applications deployed via Wodby or to clone existing public build templates.

## Auth

Wodby supports two authentication methods for GitLab:

- OAuth2 for GitLab.com
- Token authentication for GitLab.com and self-hosted GitLab

When using token authentication:

- You can use a personal, group, or project access token
- Required scopes for Git repository access: `read_api` and `read_repository`
- Use `api` instead of `read_api` if you plan to use GitLab CI features such as re-running jobs or creating new pipelines
- Required role: `Developer` or higher for both Git and CI integrations
- For self-hosted GitLab, specify the GitLab base URL. Leave it empty for GitLab.com
- If you want to run GitLab CI builds from Wodby, make sure the token's actor is allowed to run pipelines for protected branches such as `main`

## CI

Wodby supports GitLab CI as a third-party CI integration.

- You can trigger a new build from Wodby by creating a new pipeline for the same ref as the last recorded build
- You can re-run the last recorded build by retrying the associated GitLab job
- Self-hosted GitLab is supported via token authentication
