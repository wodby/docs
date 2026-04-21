# CI providers

CI providers are third-party services whose integrations expose the `ci` type. Use this group when you want builds and deploys to run from an existing CI system.

Machine name: `ci`

Use a CI provider when:

- you want builds and deploys to run from an existing CI system
- you want Wodby-aware build metadata and deployment commands inside that CI workflow
- you want to choose between Wodby's built-in CI flow and a third-party provider

## Where it is used in Wodby

CI provider integrations are used for:

- app build and deploy workflows
- organization or app defaults for CI behavior
- provider-backed actions such as triggering or rerunning supported workflows

## Supported options

| Option | Kind | Notes |
| --- | --- | --- |
| [Wodby CI](../cicd/wodby-ci.md) | Built-in | Wodby-managed CI flow |
| [CircleCI](circleci.md) | Provider | Third-party CI integration |
| [GitHub Actions](github.md#actions) | Provider | Uses the GitHub provider |
| [GitLab CI](gitlab.md#ci) | Provider | Uses the GitLab provider |

## Choosing between Wodby CI and third-party CI

- Use [Wodby CI](../cicd/wodby-ci.md) when you want the most direct Wodby-managed path.
- Use a third-party CI integration when your team already builds in GitHub Actions, GitLab CI, or CircleCI.

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [CI/CD overview](../cicd/index.md)
- [Third-party CI](../cicd/third-party.md)
