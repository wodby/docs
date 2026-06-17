# Custom CI

Custom CI is a CI provider for app instances that build in an external pipeline without connecting that CI provider to
Wodby. Use it for unsupported CI systems, self-managed pipelines, or cases where you want Wodby CLI to create and deploy
builds without provider API access.

Custom CI exposes the `ci` integration type and does not require credentials.

## Behavior

With Custom CI:

- Wodby CLI creates app builds from the app service ID.
- App services with build sources can omit a linked Git repository in Wodby.
- The CLI sends git ref, commit, author, message, build ID, build number, and a detected provider value.
- Wodby accepts any non-empty CLI provider value for the Custom CI integration, including `unknown`, `github`, `gitlab`, or `circleci`.
- Wodby does not poll the CI provider for status.
- Wodby cannot trigger new provider builds or rerun provider jobs from the dashboard.

The CI job must call `wodby ci deploy` after images are released. If the external CI job fails before deployment, Wodby
does not receive a provider status update.

## CLI provider detection

`wodby ci init` detects GitHub Actions, GitLab CI, and CircleCI when their standard environment variables are present.
For other providers, the CLI reads git metadata from the checkout and sends `provider: unknown`.

Use `--provider` to override the detected provider value. This is useful when a known CI system is intentionally used
through the Custom CI integration:

```bash
wodby ci init --provider unknown --build-id "$CI_BUILD_ID" --build-num "$CI_BUILD_NUMBER" "$WODBY_APP_SERVICE_ID"
```

Pass `--build-id` and `--build-num` when the CLI cannot detect a CI run ID and build number from the environment.

## Linked repositories

A linked Git repository is optional for app services with build sources when the app instance uses Custom CI.

If no repository is linked, Wodby trusts the git metadata sent by the CLI. If a repository is linked, Wodby can use it
as repository metadata and validate submitted refs, but provider run, rerun, and polling actions remain unavailable for
Custom CI.
