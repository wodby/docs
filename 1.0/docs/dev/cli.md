# Wodby CLI

Use **Wodby CLI 1.x** to automate Wodby 1 workflows, including [CI/CD deployments](../cicd/index.md). The CLI's [`master` branch](https://github.com/wodby/wodby-cli/tree/master) is the maintenance branch for Wodby 1.

## Platform compatibility

| Wodby platform | CLI version | Source branch |
| --- | --- | --- |
| Wodby 1 | 1.x | [`master`](https://github.com/wodby/wodby-cli/tree/master) |
| Wodby 2 | 2.x | [`2.0`](https://github.com/wodby/wodby-cli/tree/2.0) |

The CLI major version must match your Wodby platform. GitHub's **Latest** release points to Wodby 2, so select an explicit 1.x release for Wodby 1.

## Installation

Download [Wodby CLI 1.0.9](https://github.com/wodby/wodby-cli/releases/tag/1.0.9) for your operating system and architecture. See the [Wodby 1 installation instructions](https://github.com/wodby/wodby-cli/blob/master/README.md#install) for Linux, macOS, and Windows.

For container-based builds, use a versioned 1.x tag of the [`wodby/wodby-cli` image](https://hub.docker.com/r/wodby/wodby-cli/tags), such as `wodby/wodby-cli:1.0.9`.

Check the installed version with:

```shell
wodby version
```

## Usage

See the [Wodby 1 command reference](https://github.com/wodby/wodby-cli/blob/master/README.md#usage) for available commands and flags, and the [third-party CI guide](../cicd/third-party.md) for the complete build and deployment workflow.
