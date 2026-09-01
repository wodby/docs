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
- organization defaults and app environment Default CI selections for connected build sources
- provider-backed actions such as triggering or rerunning supported workflows

Provider-backed actions are available only for CI providers that Wodby can call directly. [Custom CI](custom-ci.md)
uses the same CLI build and deploy flow, but Wodby does not poll, trigger, or rerun the external CI provider.

## Starting builds from the dashboard

The dashboard's **New build** action, including the **New build** option in a new deployment, depends on the app
service's effective CI provider and build-source configuration. Connected sources inherit the app environment's Default
CI, while public and cloned boilerplate sources use Wodby CI.

| CI mode | Dashboard requirements |
| --- | --- |
| Wodby CI | A linked Git repository and ref |
| GitHub Actions | A linked Git repository and a previously recorded GitHub workflow for the app service; the workflow must support `workflow_dispatch` |
| GitLab CI | A linked Git repository and branch or tag |
| CircleCI | A linked Git repository and a previously recorded CircleCI workflow for the app service |
| Custom CI | Not available; start the build in the external pipeline |

GitHub Actions starts a fresh run using workflow identity and ref from a previously recorded build. GitLab CI starts a
fresh pipeline from the stored repository ref without requiring a previous Wodby build. CircleCI starts a dashboard
build by rerunning a recorded workflow.

## Supported options

| Option | Kind | Notes |
| --- | --- | --- |
| [Wodby CI](../cicd/wodby-ci.md) | Built-in | Wodby-managed CI flow |
| [CircleCI](circleci.md) | Provider | Third-party CI integration |
| [Custom CI](custom-ci.md) | Provider | No provider connection; build completion is driven by Wodby CLI |
| [GitHub Actions](github.md#actions) | Provider | Uses the GitHub provider |
| [GitLab CI](gitlab.md#ci) | Provider | Uses the GitLab provider |

## Choosing between Wodby CI and third-party CI

- Use [Wodby CI](../cicd/wodby-ci.md) when you want the most direct Wodby-managed path.
- Use a provider-backed third-party CI integration when your team already builds in GitHub Actions, GitLab CI, or CircleCI and you want Wodby to use provider APIs where supported.
- Use Custom CI when your team already has a CI workflow but does not want to connect that CI provider to Wodby, or when the CI provider is unsupported.

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [CI/CD overview](../cicd/index.md)
- [Third-party CI](../cicd/third-party.md)
