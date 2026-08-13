# Environment variables

Wodby compiles environment variables for each app service from its service and stack configuration, connected
services and integrations, and app-instance overrides. The effective runtime variables are injected into the
service's containers when the app instance is deployed.

## Where variables come from

Environment variables can come from several layers:

| Source | Purpose |
| --- | --- |
| Service template | Defaults and service-specific configuration supplied by the service author |
| Service settings | User-facing settings that map to environment variables |
| Service links | Connection details supplied by linked services, such as a database or cache |
| Stack | Defaults shared by app services created from a stack revision |
| Stack service | Defaults for one service in a stack revision |
| Variable integration | Reusable provider credentials and configuration attached to a stack or app service |
| App service | Overrides for one service in one app instance |

Configure app-service variables from
`Apps > [App] > [Instance] > Stack > App services > [Service] > Configuration > Variables`. Configure reusable
stack and stack-service values from the corresponding `Configuration > Variables` page in the stack.

App-service variables override inherited values with the same name and target. A variable scoped to a workload and
container overrides a global variable with the same name for that container. The dashboard shows inherited variables
alongside app-service overrides and identifies their source.

## Scope and environment types

An app-service variable can apply to the whole service or to one workload and container. A global variable is added to
every container in the app service.

Stack, stack-service, and service-template variables can be limited to an environment type. Wodby applies an
environment-specific variable only when the app instance uses a matching environment type:

- `prod`
- `staging`
- `test`
- `dev`
- `feature`

Variables without an environment type apply to every environment type.

## Runtime and build variables

App-service and service-template variables can be runtime-scoped, build-scoped, or both:

- Runtime variables are injected into deployed containers.
- Build variables are passed to CI builds as Docker build arguments when the Dockerfile declares a matching `ARG`.

At least one scope must be enabled. Build-scoped app-service variables are available only for services with build
configuration. Stack-wide, stack-service, and variable-integration values are runtime-only; use a build-scoped
app-service variable or service setting when a Dockerfile needs a value during a build.

Changing a runtime-only variable marks the app service for redeploy. Changing a build-scoped variable marks it for
rebuild.

## Secrets

Mark sensitive values as secret. Wodby stores secret environment-variable values in a Kubernetes Secret and does not
show their plaintext values in the dashboard after they are saved.

Variable integrations are useful when the same credentials or configuration must be reused across services, apps, or
environments. See [Variable integrations](../integrations/variable.md).

## System environment variables

Wodby adds the following runtime-only variables to every app-service container:

| Variable | Value |
| --- | --- |
| `WODBY` | `true`, indicating that the container runs on Wodby |
| `WODBY2` | `true`, indicating the Wodby 2 runtime |
| `WODBY_APP_NAME` | App machine name |
| `WODBY_APP_INSTANCE_NAME` | App-instance machine name |
| `WODBY_APP_SERVICE_NAME` | App-service machine name |
| `WODBY_ENV_NAME` | Name of the environment assigned to the app instance |
| `WODBY_ENV_TYPE` | Environment type: `prod`, `staging`, `test`, `dev`, or `feature` |
| `WODBY_HOSTS` | JSON array of route and active App Access hostnames accepted by the app instance |
| `WODBY_PRIMARY_HOST` | Protected primary hostname when App Access is configured; otherwise the enabled `Main` route hostname |
| `WODBY_PRIMARY_URL` | URL for `WODBY_PRIMARY_HOST`; protected App Access URLs use `https` |

`WODBY_PRIMARY_HOST` and `WODBY_PRIMARY_URL` are present only when the app instance has a primary hostname. During an
[App Access](access.md#primary-hostname) change, `WODBY_HOSTS` can temporarily contain both current and desired
hostnames so the workload continues accepting traffic throughout the transition.

## Names and reserved variables

An environment-variable name can contain letters, digits, `_`, `-`, and `.`, but cannot start with a digit.

`WODBY`, `WODBY2`, and the entire `WODBY_*` namespace are reserved for platform-managed variables. You cannot add or
override these names through app-service variables, stack variables, stack-service variables, service settings, or
custom variable-provider mappings. Service templates maintained by the platform can define additional
service-specific `WODBY_*` variables, but user configuration cannot replace the runtime identity variables listed
above.

The only user-configurable exception is `WODBY_MIGRATIONS_ADD_LEGACY_WODBY1_ENV_VARS`. The Wodby 1 migration tool sets
this marker on migrated stacks so Wodby can expose compatibility aliases expected by Wodby 1 applications:

| Wodby 1 compatibility variable | Wodby 2 source |
| --- | --- |
| `WODBY_INSTANCE_NAME` | `WODBY_APP_INSTANCE_NAME` |
| `WODBY_ENVIRONMENT_NAME` | `WODBY_APP_INSTANCE_NAME` |
| `WODBY_INSTANCE_TYPE` | `WODBY_ENV_TYPE`; `staging` is exposed as `stage` |
| `WODBY_ENVIRONMENT_TYPE` | `WODBY_ENV_TYPE`; `staging` is exposed as `stage` |
| `WODBY_HOST_PRIMARY` | `WODBY_PRIMARY_HOST` |
| `WODBY_URL_PRIMARY` | `WODBY_PRIMARY_URL` |

Do not add this marker to new Wodby 2 stacks. It exists only to keep migrated Wodby 1 applications compatible while
they are updated to use the native Wodby 2 variables.

## Related pages

- [App services](services.md)
- [Application environments](env.md)
- [Stack configuration](../stacks/configuration.md)
- [Service template environment variables](../services/template.md#environment-variable-object)
- [Variable integrations](../integrations/variable.md)
