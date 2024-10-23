# Service build

Non-external services can be buildable. Such services will expect to receive a related build info during app deployment. 

There are two main types of buildable services:

1. Services that require a git repository connected
2. Services that do not have a git repository but still expected to be built in [CI](../cicd/index.md) process

## Build templates

Services that require a git repository can also have build templates, those a public git repositories that contain a boilerplate and a pipeline. You can clone a build template repository under a selected [git integration](../integrations/index.md#git).

## Dockerfile

Services may specify a custom Dockerfile located in the same repository. This Dockerfile will be used during `wodby ci build [service]` command when [Wodby CI](../cicd/wodby-ci.md) used.
