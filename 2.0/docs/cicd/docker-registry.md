# Docker Registry

`wodby ci init` requests registry credentials for the current build and logs Docker in to the registry associated with your application.

`wodby ci release [SERVICE]...` pushes the images built during `wodby ci build`. If you do not specify services, the CLI releases all built services from the current build.

By default, Wodby uses [Wodby Registry](wodby-registry.md), but you can also attach another registry integration such as [Docker Hub](../providers/docker.md) or [Distribution Registry](../providers/distribution.md).

Built images are tagged as:

```text
[registry-host]/[registry-repository]:[service]-[build-number]
```

For Docker Hub registry integrations, the registry host is `docker.io`. The registry repository is based on the Docker Hub namespace and app instance name, for example:

```text
[namespace]/[app-name]_[app-instance-name]-[suffix]
```

Docker Hub push operations use the integration's main credentials. Deployment image pulls use the optional pull-only credentials when both pull-only fields are set; otherwise they use the main credentials.

For Distribution Registry integrations, the registry host is the normalized integration host without `http://` or `https://`. The registry repository is based on the optional repository prefix and app instance name, for example:

```text
[prefix]/[app-name]_[app-instance-name]-[suffix]
```

If the integration does not define a repository prefix, Wodby uses the organization machine name. Distribution Registry push operations use the integration's main credentials. Deployment image pulls use the optional pull-only credentials when both pull-only fields are set; otherwise they use the main credentials.

`wodby ci release` can also publish additional tags:

- `--branch-tag` pushes a Docker-compatible tag based on the current git branch. Branch names that are already valid
  Docker tags are preserved. Invalid or overlong names are converted to a readable tag with a short hash suffix so
  different branch names do not overwrite the same tag.
- `--latest-branch <branch>` updates the `latest` tag when the build comes from the selected branch
