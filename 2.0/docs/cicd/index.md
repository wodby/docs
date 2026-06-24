# CI/CD

Wodby uses the same CLI-driven workflow for both the built-in [Wodby CI](wodby-ci.md) and [third-party CI providers](third-party.md). The main difference is the identifier passed to `wodby ci init`:

- In Wodby CI, use `WODBY_BUILD_ID`. The build already exists and the CLI loads it.
- In third-party CI, use `WODBY_APP_SERVICE_ID` for the app service being built. The CLI creates a build from the CI metadata it detects.

Wodby CI installs Wodby CLI during the `Setting up build environment` step. Third-party CI jobs must install Wodby CLI
themselves before calling `wodby ci init`.

For app instances that use third-party CI, an app service with a build source does not have to link a Git repository in
Wodby. The CI provider supplies the checkout, and Wodby CLI sends commit, ref, and build metadata when it creates the
app build.

`wodby ci init` automatically detects build and git metadata from GitHub Actions, GitLab CI, and CircleCI. If the CI
provider is not recognized, the CLI reads git metadata from the checkout and sends `provider: unknown`. Pass
`--provider` to override the detected provider value, for example when the app instance uses [Custom CI](../providers/custom-ci.md).
Pass `--build-id` and `--build-num` when the CLI cannot detect a CI run ID and build number.

Initialize the pipeline with `wodby ci init $WODBY_BUILD_ID` in Wodby CI or `wodby ci init $WODBY_APP_SERVICE_ID` in third-party CI. A typical flow then looks like this:

```bash
# Optional one-off commands, for example dependency installation
wodby ci run -- composer install -n --no-ansi

# Build, push, and deploy images
wodby ci build
wodby ci release
wodby ci deploy
```

## 1. Init

`wodby ci init` creates or loads the app build, logs Docker in to the associated [registry](docker-registry.md), prepares the working directory, and reads `.wodby/post-deployment.yml` from the build context when present.

Use `--dind` when your CI provider builds through docker-in-docker. Use `--fix-permissions` only when you explicitly want the CLI to change codebase ownership.

## 2. Run commands in the build environment

`wodby ci run` starts a one-off container from a service image in your stack or from an explicitly specified image. This is typically used for dependency installation or asset compilation before `wodby ci build`.

## 3. [Build](build.md)

`wodby ci build [SERVICE]...` builds all build image targets from the current app build config or only the services you specify. The CLI can use a Dockerfile from your repository, a Dockerfile from the Wodby service configuration, or a generated default Dockerfile. It also supports build arguments, custom copy paths, and buildx cache backends.

## 4. [Release](docker-registry.md)

`wodby ci release [SERVICE]...` pushes the built images to the registry configured for the build. By default this is [Wodby Registry](wodby-registry.md), but you can also use supported [registry providers](../providers/registry.md).

## 5. [Deploy](deploy.md)

`wodby ci deploy [SERVICE]...` tells Wodby to deploy the released images. You can optionally skip post-deployment scripts with `--skip-post-deploy`.
