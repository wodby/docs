# Environment Variables

## Global

The following variables exists in all containers:

| Variable                  | Description                     |
| ------------------------- | ------------------------------- |
| `$WODBY_INSTANCE_NAME`    | Instance machine name           |
| `$WODBY_INSTANCE_TYPE`    | Instance type: dev, stage, prod |
| `$WODBY_ENVIRONMENT_TYPE` | Same as `$WODBY_INSTANCE_NAME`  |
| `$WODBY_ENVIRONMENT_TYPE` | Same as `$WODBY_INSTANCE_TYPE`  |
| `$WODBY_INSTANCE_UUID`    | Instance UUID                   |
| `$WODBY_APP_NAME`         | Application machine name        |
| `$WODBY_APP_UUID`         | Application UUID                |

## Stack-specific

See [stacks documentation](../stacks/index.md) to see stack-specific environment variables