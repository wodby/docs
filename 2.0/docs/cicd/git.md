# Git repository

You can start building apps with your own codebase by creating one of the Git integrations ([GitHub](../integrations/github.md), [GitLab](../integrations/gitlab.md), [BitBucket](../integrations/bitbucket.md)), then selecting your own git repository during new app creation (for [buildable services](../services/build.md)). Alternatively, if a service provides build templates, you can clone it to your own git repository, the build template already contains pipeline definition for [Wodby CI](wodby-ci.md). Then during the build of a service with Wodby CI command  `clone` will clone referenced git repository.

You can change a git repository and a branch/tag for existing app instance from `[App instance] > App Services > [Service]` in Build Source section.
