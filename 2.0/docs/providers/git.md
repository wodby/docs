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
- updating Git-backed stacks and services from selected branches or tags

## Push events

For supported providers, Wodby can use repository push events to start automatic work connected to the tracked Git ref.
Examples include Git-backed stack updates, Git-backed service updates, and other Git-driven automation.

Wodby currently handles push events from GitHub and GitLab integrations.

Automatic stack and service updates still follow the auto-update settings on the stack or service. A push to an
untracked branch or a tag outside the allowed semantic-version range is ignored.
Git auto-update can follow either the tracked branch or newer semantic-version tags for the tracked tag. It cannot use
both modes at the same time.

## Supported providers

| Provider | Notes |
| --- | --- |
| [GitHub](github.md) | Repositories, automated build-template import into new repositories, and GitHub Actions support |
| [GitLab](gitlab.md) | Repositories, automated build-template import into new repositories, and GitLab CI support |
| [Bitbucket](bitbucket.md) | Repositories only; build-template imports must be done manually |

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [CI providers](ci.md)
- [Git in CI/CD](../cicd/git.md)
