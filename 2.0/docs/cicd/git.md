# Git repository

Start by creating a Git integration from a supported Git provider such as [GitHub](../providers/github.md), [GitLab](../providers/gitlab.md), or [Bitbucket](../providers/bitbucket.md). When the app instance uses Wodby CI, the selected repository is the build source for an app service with [build configuration](../services/build.md). When the app instance uses third-party CI, linking the repository in Wodby is optional because the CI provider performs the checkout.

If you use [Wodby CI](wodby-ci.md), keep the pipeline definition in the repository itself:

- `.wodby/pipeline.yml`
- `.wodby/post-deployment.yml` (optional)

If you use [third-party CI](third-party.md), keep the provider-native config in the repository root, for example:

- `.github/workflows/wodby.yml`
- `.gitlab-ci.yml`
- `.circleci/config.yml`

In Wodby CI, the `clone` step checks out the repository configured as the build source. In third-party CI, the CI provider performs the checkout and Wodby CLI works from that existing workspace.

You can change the repository and the selected branch or tag for an existing app instance from the Build Source section of the app service when a repository is linked.

For example configurations, see the [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0) repository.
