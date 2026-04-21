# Git providers

Git providers are third-party services whose integrations expose the `git` type. Use this group when you want Wodby to list repositories, branches, and tags and use remote repositories as build sources.

Machine name: `git`

Use a Git provider when:

- you want to deploy from a repository hosted on a supported Git provider
- you want Wodby to discover remote branches and tags during build-source setup
- you want reusable repository access instead of entering raw clone credentials per app

## Where it is used in Wodby

Git provider integrations are used for:

- selecting remote repositories during app build-source setup
- browsing branches and tags for build configuration
- connecting app instances to provider-hosted source code

## Supported providers

| Provider | Notes |
| --- | --- |
| [GitHub](github.md) | Repositories and GitHub Actions support |
| [GitLab](gitlab.md) | Repositories and GitLab CI support |
| [Bitbucket](bitbucket.md) | Repositories only |

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [CI providers](ci.md)
- [Git in CI/CD](../cicd/git.md)
