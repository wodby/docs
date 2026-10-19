# Direct Git deployment

!!! info "Only for Drupal and WP"
    Direct git deployment is available only for [Drupal](../stacks/drupal/index.md) and [WordPress](../stacks/wordpress/index.md) stacks and their forks

You can connect your git repository to Wodby and use it as a codebase source for your applications. On code deployment we will perform pull from the target branch and run [post-deployment scripts](post-deployment-scripts.md) (if enabled).

Additionally, you can run deployment automatically every time you push code to a git branch (all instances using this branch will be deployed):

1. Configure git hooks for your git repository
2. Navigate to `Instance > Deployment > Settings` and check `Automatic deploy` option

For details instructions how to connect a repository and configure hooks see the following articles:

* [GitHub](../integrations/github.md)
* [BitBucket](../integrations/bitbucket.md)
* [GitLab](../integrations/gitlab.md)
* [Custom git provider](../integrations/custom.md)
