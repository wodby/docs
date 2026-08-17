# Building with third-party CI

If you prefer GitHub Actions, GitLab CI, CircleCI, or another CI provider, use [Wodby CLI](../dev/cli.md) inside that pipeline.

Wodby CLI automatically detects build and git metadata for:

- GitHub Actions
- GitLab CI
- CircleCI

For unsupported providers, Wodby CLI falls back to git metadata from the checkout and sends `provider: unknown`. Pass
`--build-id` and `--build-num` when the CLI cannot detect the CI run ID and build number.

Use [Custom CI](../providers/custom-ci.md) when you do not want to connect the CI provider to Wodby, or when the CI
provider is not supported directly. With Custom CI, Wodby accepts the provider value detected by the CLI, including
`unknown`, `github`, `gitlab`, or `circleci`, but does not call provider APIs for status polling, run, or rerun actions.

## Required variables

- `WODBY_API_KEY` as a secret with your [Wodby API key](../dev/api-keys.md)
- `WODBY_APP_SERVICE_ID` as the ID of the app service being built

You can find the app service ID on the Overview page of the corresponding app service.

## Source selection

When a connected build source inherits third-party Default CI, it does not have to link a Git repository in Wodby. The
CI provider checks out the code, and Wodby CLI creates the app build from the app service ID plus the git metadata it
detects in the CI workspace. In this mode, source selection belongs entirely to the external pipeline.

If you link a Git repository, you must also select a branch, tag, or commit. Wodby then accepts only CI builds that
match that repository and selected source:

- a branch or tag must match both the reported ref type and exact ref name
- a commit source must match the reported commit SHA

For example, if the linked source selects the `main` branch, a pull request workflow that checks out and reports a
feature branch cannot create a Wodby build for that service. Leave the repository unlinked only when the external
pipeline should control which refs can build and deploy.

Changing a linked repository or ref takes effect immediately. A build initialized for the previous source cannot later
be deployed with `wodby ci deploy`; start a new workflow from the currently selected source instead.

Public and cloned boilerplate sources use Wodby CI even when the instance's Default CI is third-party. They are not
initialized with `WODBY_APP_SERVICE_ID`. An app may contain both kinds of source; its deployment waits for builds from
all source owners before it starts.

## Dashboard-triggered builds

Dashboard build support is provider-specific:

- **GitHub Actions** starts a fresh `workflow_dispatch` using a previously recorded workflow for the linked repository
  and app service, and dispatches it against the selected ref. Run the first workflow on that ref outside Wodby so its
  workflow ID can be recorded. Workflows recorded from other refs are not used.
- **GitLab CI** creates a fresh pipeline for the linked repository and configured branch or tag. A previous build is not
  required.
- **CircleCI** reruns a previously recorded workflow for the linked repository, selected ref, and app service. Run the
  first workflow on that ref outside Wodby so it can be recorded.
- **Custom CI** cannot be started or rerun from the dashboard. Start it in the external CI system.

When these requirements are not met, Wodby disables **New build** and shows the missing repository, ref, previously
recorded workflow, or provider capability. Existing successful builds remain available for deployment when otherwise
compatible.

## Builds without a linked Git repository

Without a linked Git repository, Wodby cannot poll the CI provider for the build status. After `wodby ci init`, run
`wodby ci deploy` within three hours. Otherwise, Wodby marks the build as errored and cancels its awaiting deployment.
A later deploy attempt cannot reopen the expired build; restart the CI workflow so it initializes a new build and
deployment.

## Typical flow

1. Check out the repository in your CI job.
2. Install Wodby CLI and run `wodby ci init $WODBY_APP_SERVICE_ID`.
3. Use `wodby ci run ...` for dependency installation or other one-off commands.
4. Run `wodby ci build [SERVICE]...`.
5. Run `wodby ci release [SERVICE]...`.
6. Run `wodby ci deploy [SERVICE]...`.

Use `wodby ci init --dind $WODBY_APP_SERVICE_ID` when your provider builds through docker-in-docker, as in the GitLab CI examples.

If your app instance uses Custom CI but the job runs in a known provider such as GitHub Actions or GitLab CI, either let
the CLI send the detected provider value or force a generic value:

```bash
wodby ci init --provider unknown --build-id "$CI_BUILD_ID" --build-num "$CI_BUILD_NUMBER" "$WODBY_APP_SERVICE_ID"
```

If your app uses secret build-scoped environment variables, define matching secret environment variables in the CI
provider. Wodby CLI forwards secret build args from the CI environment instead of storing their values in the local
build config.

## Provider examples

The [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0) repository contains complete provider examples for
common PHP, Node.js, Python, Ruby, Go, and static application patterns:

- GitHub Actions examples use [`wodby/actions/setup-wodby-cli@v1`](https://github.com/wodby/actions/tree/main/setup-wodby-cli), which restores dependency caches detected from lockfiles, installs the CLI, exports `WODBY_API_KEY`, and runs `wodby ci init` automatically when `app-service-id` is provided.
- CircleCI examples use [`wodby/setup-wodby-cli@1`](https://circleci.com/developer/orbs/orb/wodby/setup-wodby-cli), which installs the latest Wodby 2 CLI and runs `wodby ci init` when `app-service-id` is provided.
- GitHub Actions: [PHP](https://github.com/wodby/wodby-ci/blob/2.0/php/github-actions/wodby.yml), [Node](https://github.com/wodby/wodby-ci/blob/2.0/node/github-actions/wodby.yml)
- GitLab CI: [PHP](https://github.com/wodby/wodby-ci/blob/2.0/php/gitlab-ci/.gitlab-ci.yml), [Node](https://github.com/wodby/wodby-ci/blob/2.0/node/gitlab-ci/.gitlab-ci.yml)
- CircleCI: [PHP](https://github.com/wodby/wodby-ci/blob/2.0/php/circleci/config.yml), [Node](https://github.com/wodby/wodby-ci/blob/2.0/node/circleci/config.yml)

For providers that support both VM-based and docker-based execution, prefer VM-based runners because Docker image builds are more straightforward without docker-in-docker. The CircleCI examples use the machine executor for that reason.

On native runners, such as the CircleCI machine executor, the CLI mounts recognized caches from the package managers'
conventional home paths: `~/.npm`, `~/.composer/cache`, `~/.bundle/cache`, and `~/.cache/uv`. Configure the provider to
persist the applicable path; no manual `wodby ci run` cache volume is required. The GitHub setup action handles these
paths automatically when it detects a supported lockfile. The CircleCI examples restore and save the applicable path
in their configuration.

Docker-in-docker examples, such as GitLab CI with the `docker:dind` service, instead persist project-local
`.wodby-ci-cache/<profile>` staging directories. The CLI imports them into its internal cache volume during
`wodby ci init` and exports updated contents after cache-enabled commands. Set `WODBY_CI_CACHE_DIR` only when an
environment requires a different root. This persistence is optional: the directory does not need to exist before the
job, and an automatic cache import, setup, or export failure only produces a warning.

## Post-deployment scripts

You can still use [`.wodby/post-deployment.yml`](wodby-ci.md#post-deployment-scripts) with third-party CI. Wodby CLI reads it during `wodby ci init` and attaches it to the build. Pass `--skip-post-deploy` to `wodby ci deploy` when you want to skip those jobs.
