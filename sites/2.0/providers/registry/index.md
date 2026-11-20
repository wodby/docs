Source: https://wodby.com/docs/2.0/providers/registry/

# Registry providers

Registry providers are third-party services whose integrations expose the `registry` type. Use this group when you want build output and deployment images stored in an external container registry.

Machine name: `registry`

Use a registry provider when:

- you want built images pushed to an external registry
- you want app builds and deploys to pull from a registry outside Wodby Registry
- you want a reusable registry connection at organization or app level

## Where it is used in Wodby

Registry provider integrations are used for:

- app image build and push workflows
- organization defaults for container image storage
- app environment registry selection when builds should use a specific external registry

## Supported options

| Option | Kind | Notes |
| --- | --- | --- |
| [Wodby Registry](https://wodby.com/docs/2.0/cicd/wodby-registry/) | Built-in | Default Wodby-managed registry flow |
| [Docker Hub](https://wodby.com/docs/2.0/providers/docker/) | Provider | Hosted public or private Docker Hub registries |
| [Distribution Registry](https://wodby.com/docs/2.0/providers/distribution/) | Provider | Generic registry implementing the Docker distribution API |

## Related pages

- [Integration types](https://wodby.com/docs/2.0/integrations/types/)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
- [Container Registry in CI/CD](https://wodby.com/docs/2.0/cicd/docker-registry/)
- [Wodby Registry](https://wodby.com/docs/2.0/cicd/wodby-registry/)
