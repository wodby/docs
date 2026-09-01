# Git repository

Start by creating a Git integration from a supported Git provider such as [GitHub](../providers/github.md),
[GitLab](../providers/gitlab.md), or [Bitbucket](../providers/bitbucket.md). A connected build source inherits the app
environment's Default CI. Under Wodby CI, its selected repository and ref are required. Under third-party CI, linking the
repository in Wodby is optional because the CI provider performs the checkout. When you link or edit it, you must select
a branch, tag, or commit; Wodby accepts only CI builds that match that source. Leave it unlinked when source selection
should remain entirely in the external pipeline. Public and cloned boilerplate sources use Wodby CI regardless of
Default CI.

## Repository authentication

Wodby CI clones connected Git-provider repositories over HTTPS and authenticates with the connected integration.

Wodby does not inject a shared SSH private key into builds. An SSH clone URL requires an app-service-specific private
key named `id_rsa`; without that key, use the connected repository's HTTPS clone URL instead. Keys configured for one
app service are not shared with other app services.

If you use [Wodby CI](wodby-ci.md), keep the pipeline definition in the repository itself:

- `.wodby/pipeline.yml`
- `.wodby/post-deployment.yml` (optional)

If you use [third-party CI](third-party.md), keep the provider-native config in the repository root, for example:

- `.github/workflows/wodby.yml`
- `.gitlab-ci.yml`
- `.circleci/config.yml`

In Wodby CI, the `clone` step checks out the repository configured as the build source. In third-party CI, the CI provider performs the checkout and Wodby CLI works from that existing workspace.

You can change the repository and the selected branch, tag, or commit for an existing app environment from the Build
Source section of the app service when a repository is linked. See [third-party CI source selection](third-party.md#source-selection)
for how these changes affect CI build admission and deployment.

For example configurations, see the [`wodby/wodby-ci`](https://github.com/wodby/wodby-ci/tree/2.0) repository.
