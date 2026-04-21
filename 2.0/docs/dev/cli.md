# Wodby CLI

The official Wodby CLI is focused on CI workflows. It creates or loads builds, logs in to the registry, builds images, releases them, deploys them, and runs one-off containers in the build context.

Repository: <https://github.com/wodby/wodby-cli>

## Install

Install the latest release from the project releases page:

- <https://github.com/wodby/wodby-cli/releases>

The CLI currently exposes a small top-level surface:

- `ci`
- `completion`
- `help`
- `version`

## Authentication and configuration

Common public configuration options:

| Input | Env var | Flag | Notes |
| --- | --- | --- | --- |
| API key | `WODBY_API_KEY` | `--api-key` | Recommended for user automation |
| CI config path | none | `--ci-config-path` | Defaults to `/tmp/.wodby-ci.json` |
| Verbose logging | none | `--verbose` | Enables debug output |

For public usage, authenticate the CLI with an API key.

## Typical flow

```bash
export WODBY_API_KEY=...

wodby ci init 12345
wodby ci build php nginx
wodby ci release php nginx
wodby ci deploy php nginx
```

If you want to run a one-off command inside the build context before building, add:

```bash
wodby ci run --service php composer install -n --no-ansi
```

## `wodby ci init`

`wodby ci init [OPTIONS] WODBY_APP_SERVICE_ID|WODBY_BUILD_ID`

This command:

- creates a new build from CI metadata when you pass an app service ID
- loads an existing build when the workflow is already running inside Wodby CI
- logs Docker in to the registry associated with that build
- discovers the main service working directory
- writes the local CI state file to `/tmp/.wodby-ci.json` unless overridden

It also reads `.wodby/post-deployment.yml` from the build context and attaches it to the build when present.

Important behaviors:

- GitHub Actions, GitLab CI, and CircleCI metadata is auto-detected
- outside those providers, pass explicit `--build-id`, `--build-num`, and `--provider` values when detection cannot infer them
- `--dind` switches the workflow into docker-in-docker mode and copies the build context into a data container
- `--fix-permissions` changes codebase permissions only when passed explicitly

Flags:

```text
-i, --build-id string   Custom build id when auto-detection cannot determine it
-n, --build-num int     Custom build number when auto-detection cannot determine it
-c, --context string    Build context directory (default: current directory)
    --dind              Use docker-in-docker workflow with a data container
    --fix-permissions   Fix codebase permissions explicitly
    --provider string   Custom CI provider name when auto-detection cannot determine it
```

## `wodby ci build`

`wodby ci build [OPTIONS] [SERVICE]...`

Builds one or more services from the local CI config. If you do not name any services, the CLI attempts to build all services defined in the build config.

Build behavior:

- uses a service-specific Dockerfile from the build context when present
- otherwise uses the Dockerfile from the Wodby app-service config when available
- otherwise generates a default Dockerfile
- writes temporary `Dockerfile` and `.dockerignore` files only when needed
- builds through `docker buildx build --load`, so the image stays available locally for `wodby ci release`

Cache-related flags:

```text
    --cache-backend string        Build cache backend: auto, local, registry, none
    --cache-dir string            Local cache directory
    --cache-ref string            Registry cache reference
    --cache-mode string           Cache export mode
    --cache-from stringArray      Additional low-level buildx cache sources
    --cache-to stringArray        Additional low-level buildx cache destinations
```

Other useful flags:

```text
    --build-arg stringArray       Extra docker build args in NAME=VALUE form
    --build-arg-env stringArray   Forward environment variables as docker build args
-f, --dockerfile string           Relative path to Dockerfile
    --from string                 Relative source path in the build context
    --to string                   Destination path inside the image
```

## `wodby ci release`

`wodby ci release [SERVICE...]`

Pushes built images to the registry configured for the build. If no services are specified, all built services are released.

Useful flags:

```text
-b, --branch-tag             Additionally push a tag based on the current git branch
-l, --latest-branch string   Update the `latest` tag when built from this branch
```

## `wodby ci deploy`

`wodby ci deploy [SERVICE...]`

Deploys released images back to Wodby. If no services are specified, all released services are deployed.

Useful flag:

```text
    --skip-post-deploy   Skip post-deployment scripts
```

## `wodby ci run`

`wodby ci run [OPTIONS] -s SERVICE | -i IMAGE COMMAND [ARG...]`

Runs a one-off container using either:

- a service image from the current Wodby build config
- an explicitly supplied image
- the main service image when neither `--service` nor `--image` is provided

Useful flags:

```text
    --entrypoint string   Override entrypoint
-e, --env strings         Environment variables
    --env-file string     Environment file
-i, --image string        Image
-p, --path string         Working directory relative to the image working dir
-s, --service string      Service name
-u, --user string         User override
-v, --volume strings      Extra bind mounts
```

Runtime behavior worth knowing:

- with a normal host-mounted context, the CLI maps the current host `uid:gid` unless you override `--user`
- if the current host user is `1000:1000`, it leaves the image default user unchanged
- when the effective Docker user is numeric and no explicit `--entrypoint` is set, the CLI clears the image entrypoint
- in `--dind` mode, the codebase is mounted from the data container instead of the host filesystem

## Related pages

- [Wodby API](api.md)
- [CI/CD overview](../cicd/index.md)
- [Third-party CI](../cicd/third-party.md)
