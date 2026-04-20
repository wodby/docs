# Git repository

Start by connecting one of the Git integrations ([GitHub](../integrations/github.md), [GitLab](../integrations/gitlab.md), [BitBucket](../integrations/bitbucket.md)) and selecting the repository as the build source for a [buildable service](../services/build.md).

If you use [Wodby CI](wodby-ci.md), keep the pipeline definition in the repository itself:

- `.wodby/pipeline.yml`
- `.wodby/post-deployment.yml` (optional)

If you use [third-party CI](third-party.md), keep the provider-native config in the repository root, for example:

- `.github/workflows/wodby.yml`
- `.gitlab-ci.yml`
- `.circleci/config.yml`

In Wodby CI, the `clone` step checks out the repository configured as the build source. In third-party CI, the provider performs the checkout and Wodby CLI works from that existing workspace.

You can change the repository and branch or tag for an existing app instance from `[App instance] > App Services > [Service]` in the Build Source section.

For example configurations see the [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0) repository.
