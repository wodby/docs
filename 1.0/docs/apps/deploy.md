# Code deployment

Choose a deployment workflow for your app instance, then manage its builds and stored images.

<span id="direct-git-integration"></span>

## Direct git deployments

Use [Direct Git deployment](../cicd/git.md) to pull code from a connected repository
for Drupal or WordPress stacks and their forks. The guide covers repository setup,
automatic deployment on pushes, and post-deployment scripts.

## CI/CD

Use [third-party CI](../cicd/third-party.md) when your application needs a build stage,
dependency installation, tests, or a custom stack with CI-enabled services.
The guide covers the complete Wodby CLI workflow and provider examples.

### Via third-party CI

Follow the steps in the [third-party CI guide](../cicd/third-party.md):

- <span id="wodby-cli"></span>[Install Wodby CLI](../cicd/third-party.md#wodby-cli).
- <span id="init"></span>[Initialize the build](../cicd/third-party.md#init) for your app instance.
- <span id="build"></span>[Build service images](../cicd/third-party.md#build).
- <span id="dependency-caches"></span>[Configure dependency caches](../cicd/third-party.md#dependency-caches).
- <span id="release"></span>[Release images](../cicd/third-party.md#release) to a container registry.
- <span id="deploy"></span>[Deploy the build](../cicd/third-party.md#deploy).
- <span id="examples"></span>See [CI provider examples](../cicd/third-party.md#examples).

## Automatically clean unused build images

Use [Builds settings](builds.md#automatically-clean-unused-build-images) to configure retention, or [void unused build images](builds.md#void-unused-build-images) manually.

## Deploy a previous build

Open the [Builds tab](builds.md) to review history and [deploy a previous build](builds.md#deploy-a-previous-build). The guide explains eligibility, stack changes, and recovery precautions.
