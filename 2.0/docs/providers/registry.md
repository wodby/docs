# Registry providers

Registry providers are third-party services whose integrations expose the `registry` type. Use this group when you want build output and deployment images stored in an external container registry.

Machine name: `registry`

Use a registry provider when:

- you want built images pushed to an external registry
- you want app builds and deploys to pull from a registry outside Wodby Registry
- you want a reusable registry connection at organization or app level

## Where it is used in Wodby

Registry provider integrations are used for:

- app build and release workflows
- organization defaults for container image storage
- app-level registry selection when builds should use a specific external registry

## Supported options

| Option | Kind | Notes |
| --- | --- | --- |
| [Wodby Registry](../cicd/wodby-registry.md) | Built-in | Default Wodby-managed registry flow |
| [Docker Hub](docker.md) | Provider | Hosted public or private Docker Hub registries |
| [Distribution Registry](distribution.md) | Provider | Generic registry implementing the Docker distribution API |

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [Docker Registry in CI/CD](../cicd/docker-registry.md)
- [Wodby Registry](../cicd/wodby-registry.md)
