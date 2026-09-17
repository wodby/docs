# CI/CD

Wodby 1 supports direct Git deployment and container-image builds through third-party CI tools.

## Choose a deployment workflow

- [Direct Git deployments](git.md) pull code from a connected repository and can run automatically on pushes. This workflow is available for Drupal and WordPress stacks and their forks.
- [Third-party CI](third-party.md) uses the Wodby CLI to initialize, build, release, and deploy service images. Use it when you need dependency installation, tests, or a custom stack with CI-enabled services.

## Configure your pipeline

1. Choose a [deployment workflow](../apps/deploy.md) for your app instance.
2. For CI builds, create an [API key](../user/api-keys.md) scoped to the app's organization and store it in your CI provider's secret settings.
3. [Build](third-party.md#build) your service images and [release](third-party.md#release) them to Wodby's registry or an external registry. Add a [container registry integration](docker-registry.md) when deploying images from a private external registry.
4. [Deploy](third-party.md#deploy) the build and configure [post-deployment scripts](post-deployment-scripts.md) if your PHP stack needs them.

## Manage builds

See [build-image retention](../apps/deploy.md#automatically-clean-unused-build-images) to clean up unused images and [deploying a previous build](../apps/deploy.md#deploy-a-previous-build) to release saved service images again. Registry storage is covered under [Billing](../billing.md#container-registry-storage).
