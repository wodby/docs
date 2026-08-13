# CI/CD

Wodby uses the same CLI-driven workflow for both the built-in [Wodby CI](wodby-ci.md) and [third-party CI providers](third-party.md). The main difference is the identifier passed to `wodby ci init`:

- In Wodby CI, use `WODBY_BUILD_ID`. The build already exists and the CLI loads it.
- In third-party CI, use `WODBY_APP_SERVICE_ID` for the app service being built. The CLI creates a build from the CI metadata it detects.

Wodby CI installs Wodby CLI during the `Setting up build environment` step. Third-party CI jobs must install Wodby CLI
themselves before calling `wodby ci init`.

## Organization defaults, app instances, and services

Organization owners and admins can select the default CI provider and container registry from
[`Organization > Settings`](../org.md#settings). The selectors offer Wodby's built-in services and available
organization-owned integrations of the corresponding type.

New app and new app instance forms start with these defaults. You can override either selection while creating the
instance without changing the organization setting. Each instance stores the resulting selections independently, so
changing an organization default does not update existing instances or builds.

The instance CI selection is the **Default CI** for connected build sources. A service that uses a public boilerplate
or clones a boilerplate into a new repository uses Wodby CI instead. This lets one app instance contain Wodby CI and
third-party CI build sources at the same time. The container registry remains an instance-wide selection.

Change an existing instance from `Apps > [App] > [Instance] > Settings > CI/CD`. Changing Default CI applies to future
builds for connected sources that inherit it; boilerplate sources continue to use Wodby CI. Historical builds retain
their recorded CI provider, registry, and registry repository.

If no external default is configured, new instances use [Wodby CI](wodby-ci.md) and
[Wodby Registry](wodby-registry.md).

For connected sources that inherit third-party CI, an app service does not have to link a Git repository in Wodby. The
CI provider supplies the checkout, and Wodby CLI sends commit, ref, and build metadata when it creates the app build.
Public and cloned boilerplate sources require their Wodby CI pipeline and Git source.

When a build or deployment includes services using both CI paths, Wodby starts the Wodby CI builds and the supported
third-party builds as one operation. Deployment waits until every service that owns a build source has provided a
deployable build.

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

Use `--dind` when your CI provider builds through docker-in-docker. In that mode the CLI prepares internal code and
cache volumes; it does not depend on the Docker daemon being able to see host paths from inside the CLI container.
The CLI resolves the main service image user to a numeric user and group, then prepares the code volume with its
utility image. The application image does not need to provide `chown`, a shell, or a special entrypoint, and subsequent
commands continue to use the selected image's default user and entrypoint.

For a normal bind-mounted build context, the CLI does not change checkout ownership automatically. Use
`--fix-permissions` only when you explicitly want it to recursively change codebase ownership to the main service image
user.

## 2. Run commands in the build environment

`wodby ci run` starts a one-off container from a service image in your stack or from an explicitly specified image. This is typically used for dependency installation or asset compilation before `wodby ci build`.

With a bind-mounted build context, the CLI resolves the workspace's numeric user and group. If the workspace UID
matches the selected image's default UID, the CLI keeps the image's default user and entrypoint. If the UIDs differ,
the CLI runs the command as the workspace user and group, clears the image entrypoint, and sets `HOME=/tmp`. If the CLI
itself runs as root in a container but the workspace has a non-root owner, it uses that workspace owner. This keeps
generated files owned by the checkout user without recursively changing existing ownership. Explicit `--user`,
`--entrypoint`, and `HOME` values take precedence.

For supported Node.js, PHP, Ruby, and Python images, the CLI configures npm, Composer, Bundler, or uv download caches
automatically:

| Profile | Package manager variable | Container path | Native host path |
| --- | --- | --- | --- |
| `npm` | `NPM_CONFIG_CACHE` | `/tmp/wodby-cache/npm` | `~/.npm` |
| `composer` | `COMPOSER_CACHE_DIR` | `/tmp/wodby-cache/composer` | `~/.composer/cache` |
| `bundler` | `BUNDLE_USER_CACHE` | `/tmp/wodby-cache/bundler` | `~/.bundle/cache` |
| `uv` | `UV_CACHE_DIR` | `/tmp/wodby-cache/uv` | `~/.cache/uv` |

When the CLI runs natively against the host Docker daemon, it bind-mounts each profile from the package manager's
conventional path under the current user's home directory. Configure the CI provider to persist the applicable native
host path. Cache support is declared by Wodby image metadata, with compatibility detection for older Wodby images and
selected official images. Cache ownership is handled separately from the container runtime user: the CLI keeps using
the resolved workspace user and group when preparing host cache directories, including when a matching image UID means
that no Docker `--user` override is needed.

In docker-in-docker mode, commands keep the image's default user and entrypoint. The CLI uses a shared internal
`/tmp/wodby-cache` volume, imports persisted cache contents during `wodby ci init`, and exports updated profiles back to
project-local `.wodby-ci-cache/<profile>` staging directories after each cache-enabled `wodby ci run`. Configure the CI
provider to persist the applicable staging directory and add `.wodby-ci-cache/` to `.gitignore`. The staging directory
is automatically excluded from Docker build contexts.

Cache persistence is optional. Missing staging directories require no setup, and failures while importing, preparing,
or exporting automatically detected caches produce a warning instead of failing initialization or the command. A
profile explicitly requested with `--cache PROFILE` remains strict during command setup and export.

Use `--cache npm`, `--cache composer`, `--cache bundler`, or `--cache uv` to force a profile for another image. Use
`--no-cache` to disable automatic caching. Setting `WODBY_CI_CACHE_DIR` explicitly replaces the default native home
paths or docker-in-docker staging root with a `ROOT/<profile>` layout. Explicit package-manager cache environment
variables and volumes targeting the container paths above take precedence. Specifying `--user` disables automatic
profile detection; combine it with `--cache PROFILE` when both overrides are needed.

## 3. [Build](build.md)

`wodby ci build [SERVICE]...` builds all build image targets from the current app build config or only the services you specify. The CLI can use a Dockerfile from your repository, a Dockerfile from the Wodby service configuration, or a generated default Dockerfile. It also supports build arguments, custom copy paths, and buildx cache backends.

## 4. [Release](docker-registry.md)

`wodby ci release [SERVICE]...` pushes the built images to the registry configured for the build. By default this is [Wodby Registry](wodby-registry.md), but you can also use supported [registry providers](../providers/registry.md).

## 5. [Deploy](deploy.md)

`wodby ci deploy [SERVICE]...` tells Wodby to deploy the released images. You can optionally skip post-deployment scripts with `--skip-post-deploy`.
