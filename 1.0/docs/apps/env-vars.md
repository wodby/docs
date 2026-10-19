# Environment Variables

## Global

The following variables exist in all containers:

| Variable                  | Description                     |
| ------------------------- | ------------------------------- |
| `$WODBY_INSTANCE_NAME`    | Instance machine name           |
| `$WODBY_INSTANCE_TYPE`    | Instance type: dev, stage, prod |
| `$WODBY_ENVIRONMENT_NAME` | Same as `$WODBY_INSTANCE_NAME`  |
| `$WODBY_ENVIRONMENT_TYPE` | Same as `$WODBY_INSTANCE_TYPE`  |
| `$WODBY_INSTANCE_UUID`    | Instance UUID                   |
| `$WODBY_APP_NAME`         | Application machine name        |
| `$WODBY_APP_UUID`         | Application UUID                |

You can add variables named `WODBY`, `WODBY2`, or beginning with `WODBY_` in
an app instance's service configuration. A configured variable with the same
name as a generated variable overrides the generated value for that service.

## Stack-specific

See [stacks documentation](../stacks/index.md) to see stack-specific environment variables
