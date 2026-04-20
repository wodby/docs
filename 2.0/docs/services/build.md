# Service build

## Overview

Only services of type `service` can define a build section.

Use build settings when a service must be built in [CI/CD](../cicd/index.md) before deployment.

There are two common cases:

1. Services that require a connected git repository
2. Services that are still built in [CI/CD](../cicd/index.md) but do not need a repository connection

### Build templates

Build templates are starter repositories that customers can clone when creating a new project. Each template points to
a GitHub repository and selects either a branch or a tag. A template can also reference a custom pipeline file.

### Dockerfile

Services may specify a custom Dockerfile path in the same repository. Wodby CI uses it during
`wodby ci build [service]`.

## Template

Build information is defined under the [`build` section](template.md#build) in a service template.
