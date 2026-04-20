# Docker Registry

`wodby ci init` requests registry credentials for the current build and logs Docker in to the registry associated with your application.

`wodby ci release [SERVICE]...` pushes the images built during `wodby ci build`. If you do not specify services, the CLI releases all built services from the current build.

By default Wodby uses [Wodby Registry](wodby-registry.md), but you can also attach another registry integration such as [Docker Hub](../integrations/docker.md) or [Distribution](../integrations/distribution.md).

Built images are tagged as:

```text
[registry-host]/[registry-repository]:[service]-[build-number]
```

`wodby ci release` can also publish additional tags:

- `--branch-tag` pushes a tag based on the current git branch
- `--latest-branch <branch>` updates the `latest` tag when the build comes from the selected branch
