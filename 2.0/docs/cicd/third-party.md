# Building with third-party CI

If you prefer GitHub Actions, GitLab CI, CircleCI, or another CI provider, use [Wodby CLI](../dev/cli.md) inside that pipeline.

Wodby CLI automatically detects build and git metadata for:

- GitHub Actions
- GitLab CI
- CircleCI

For any other provider, pass `--build-id`, `--build-num`, and `--provider` to `wodby ci init` so Wodby can identify the build correctly.

## Required variables

- `WODBY_API_KEY` as a secret with your [Wodby API key](../dev/api-keys.md)
- `WODBY_APP_SERVICE_ID` as the ID of the buildable app service you want the pipeline to build and deploy

You can find the app service ID on the Overview page of the corresponding app service.

## Typical flow

1. Check out the repository in your CI job.
2. Install Wodby CLI and run `wodby ci init $WODBY_APP_SERVICE_ID`.
3. Use `wodby ci run ...` for dependency installation or other one-off commands.
4. Run `wodby ci build [SERVICE]...`.
5. Run `wodby ci release [SERVICE]...`.
6. Run `wodby ci deploy [SERVICE]...`.

Use `wodby ci init --dind $WODBY_APP_SERVICE_ID` when your provider builds through docker-in-docker, as in the GitLab CI examples.

## Provider examples

The [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0) repository contains complete examples for PHP and Node apps:

- GitHub Actions examples use [`wodby/actions/setup-wodby-cli@v1`](https://github.com/wodby/actions/tree/main/setup-wodby-cli), which installs the CLI, exports `WODBY_API_KEY`, and runs `wodby ci init` automatically when `app-service-id` is provided.
- GitHub Actions: [PHP](https://github.com/wodby/wodby-ci/blob/2.0/php/github-actions/wodby.yml), [Node](https://github.com/wodby/wodby-ci/blob/2.0/node/github-actions/wodby.yml)
- GitLab CI: [PHP](https://github.com/wodby/wodby-ci/blob/2.0/php/gitlab-ci/.gitlab-ci.yml), [Node](https://github.com/wodby/wodby-ci/blob/2.0/node/gitlab-ci/.gitlab-ci.yml)
- CircleCI: [PHP](https://github.com/wodby/wodby-ci/blob/2.0/php/circleci/config.yml), [Node](https://github.com/wodby/wodby-ci/blob/2.0/node/circleci/config.yml)

For providers that support both VM-based and docker-based execution, prefer VM-based runners because Docker image builds are more straightforward without docker-in-docker. The CircleCI examples use the machine executor for that reason.

## Post-deployment scripts

You can still use [`.wodby/post-deployment.yml`](wodby-ci.md#post-deployment-scripts) with third-party CI. Wodby CLI reads it during `wodby ci init` and attaches it to the build. Pass `--skip-post-deploy` to `wodby ci deploy` when you want to skip those jobs.
