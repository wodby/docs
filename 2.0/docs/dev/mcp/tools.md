# MCP tools

Use the connected server's `tools/list` response for input schemas and currently available tools. Do not assume
an operation exists because a newer skill mentions it. See [MCP setup](../mcp.md) and the
[technical reference](reference.md) for connection and response handling.

Wodby MCP tools are grouped by scope. Destructive and high-impact tools also require a `confirm: true` argument.

## Read tools

These tools require `mcp:read` when using OAuth.

| Tool | Use |
| --- | --- |
| `get_wodby_guidance` | Discover Wodby 2 workflow skills or load one by name. |
| `get_current_user` | Get the authenticated user, default organization, default projects, and available organizations. |
| `list_orgs` | List organizations available to the authenticated user. |
| `list_projects` | List projects in an organization by organization name or ID. |
| `list_envs` | List environments in an organization for app and app environment creation. |
| `list_integrations` | List integrations, optionally filtered by type, status, project, or provider labels. |
| `list_apps` | List apps in an organization, optionally filtered by project names or IDs. |
| `show_app_status` | Return a dashboard-style app summary with app environments, services, latest build, latest deployment, operational needs, and follow-up suggestions for active tasks. |
| `get_app` | Get an app by ID. |
| `find_environment` | Find an app environment by organization, app name, and the legacy `instanceName` argument. |
| `list_app_instances` | List app environments with optional project, app, cluster, and status filters by names or IDs. |
| `get_app_instance` | Get an app environment by ID. |
| `prepare_app_creation` | Resolve defaults and return missing questions for creating an app and initial app environment. This does not create anything. |
| `prepare_app_instance_creation` | Resolve defaults and return missing questions for creating an app environment in an existing app. This does not create anything. |
| `list_app_services` | List services for an app environment by app environment ID or the legacy organization/app/instance-name arguments. |
| `get_app_service` | Get an app service by ID. |
| `list_app_service_cron_schedules` | List cron schedules for an app environment or app service by IDs or by the legacy organization/app/instance-name/service arguments. |
| `list_app_builds` | List recent builds for an app environment by ID or the legacy organization/app/instance-name arguments. |
| `get_app_build` | Get an app build by ID. |
| `list_recent_deployments` | List recent deployments for an app environment by ID or the legacy organization/app/instance-name arguments. |
| `get_deployment` | Get deployment status, task, and service deployment details. |
| `get_task` | Get task jobs and steps, with follow-up suggestions when task results point to builds or deployments. |
| `wait_for_task` | Poll a task until it reaches a terminal state and optionally include bounded logs and follow-up suggestions. |
| `get_task_logs` | Get structured task job and step logs. |
| `get_task_step_logs` | Read a bounded page of live or historical task-step logs with sequence cursors. |
| `diagnose_failed_deployment` | Inspect a deployment, find failed task steps, and return relevant log excerpts. |
| `list_clusters` | List clusters in an organization. |
| `get_cluster` | Get a cluster by ID. |
| `get_kubernetes_cluster_options` | Get provider-backed Kubernetes regions or zones, machine types, versions, and settings for a Kubernetes integration. |
| `get_wodby_cloud_options` | Get Wodby Cloud regions, machine types, pricing, and creation notes. |
| `prepare_cluster_creation` | Resolve defaults and return missing questions for creating managed, k3s, demo, or Wodby Cloud clusters. This does not create anything. |
| `get_cluster_metrics` | Get a current cluster metrics summary. |
| `list_cluster_node_metrics` | List node metrics for a cluster. |
| `list_databases` | List databases in an organization. |
| `get_database` | Get a database by ID. |
| `list_database_dbs` | List DBs inside a database. |
| `list_database_users` | List database users without returning passwords. |
| `list_public_services` | List public service catalog items. |
| `list_services` | List services in an organization. |
| `get_service` | Get a service by name and optional revision number. |
| `get_service_contract` | Inspect revision-specific resolved service metadata; configuration values and source contents are omitted. Not an editable manifest. |
| `get_service_schema` | Get the Wodby service manifest JSON schema. |
| `get_service_examples` | Get concise Wodby service manifest examples. |
| `validate_service_manifest` | Validate a Wodby service manifest without creating it. |
| `get_provider_schema` | Get the Wodby custom provider manifest JSON schema. |
| `validate_provider_manifest` | Validate a Wodby custom provider manifest without creating it. |
| `list_public_stacks` | List public stack catalog items. |
| `list_stacks` | List stacks in an organization. |
| `get_stack` | Get a stack by name and optional revision number. |
| `get_stack_contract` | Inspect revision-specific stack composition, links, options, and service metadata without configuration values. Not an editable manifest. |
| `get_stack_schema` | Get the Wodby stack manifest JSON schema. |
| `get_stack_examples` | Get concise Wodby stack manifest examples. |
| `validate_stack_manifest` | Validate a Wodby stack manifest without creating it. |
| `get_app_service_pods` | Get Kubernetes pod status for an app service selected by ID or by service name with an app environment selector. |
| `get_app_service_logs` | Read bounded current or previous-container logs and return a log-access task ID. |
| `start_app_service_log_watch` | Open an audited, short-lived watch for new logs from one pod and container execution. |
| `read_app_service_log_watch` | Read cursor-based batches, including dropped-entry counts and watch status. |
| `stop_app_service_log_watch` | Stop a watch without changing the application. |
| `get_app_services_metrics` | Get current metrics for one or more app services selected by IDs or by service names with an app environment selector. |
| `get_app_instances_metrics` | Get current metrics for one or more app environments. |

## Operation tools

These tools require `mcp:operate` when using OAuth.

| Tool | Use |
| --- | --- |
| `create_deployment` | Create a deployment for one or more app services selected by IDs or by service names with an app environment selector, and suggest waiting for its task. |
| `redeploy_deployment` | Redeploy from an existing deployment. |
| `deploy_build` | Deploy a completed app build. |
| `create_builds` | Create builds for one or more app services selected by IDs or by service names with an app environment selector, and suggest waiting for the build task. |
| `run_app_service_action` | Run a named action on an app service selected by ID or by service name with an app environment selector. |
| `run_app_service_cron` | Run a cron schedule immediately by schedule ID or by schedule title with an app service selector. |
| `create_backup` | Create a backup for an app service or database DB. |
| `repeat_task` | Rerun an existing task. |
| `update_current_user` | Update the authenticated user's display name. |
| `duplicate_stack` | Duplicate a stack into an organization and optional project. |

## Container command tools

These tools require OAuth with the separate `mcp:exec` scope, including result reads. Ordinary API keys cannot use
them. Execution is available only in enabled, eligible environments; see [access, limits, and recovery](reference.md#container-commands).

| Tool | Use |
| --- | --- |
| `prepare_app_service_command` | Prepare an exact command for one workload, container, and pod without starting it. |
| `exec_app_service_command` | Consume a prepared execution ID once with identical arguments. Requires `confirm: true`. |
| `get_app_service_command` | Retrieve retained state and output using the original credential, without executing again. |

## Configuration tools

These tools require `mcp:configure` when using OAuth. Tools marked here with `confirm: true` make high-impact
configuration changes.

| Tool | Use |
| --- | --- |
| `update_cluster` | Update a cluster title. |
| `update_cluster_settings` | Update cluster settings such as automatic infrastructure upgrades. Requires `confirm: true`. |
| `update_k3s_cluster_public_ip` | Update the public IP for a self-hosted k3s cluster. Requires `confirm: true`. |
| `update_database` | Update a database title. |
| `update_database_user_dbs` | Update DB grants for a database user. Requires `confirm: true`. |
| `update_service_from_manifest` | Update an existing non-Git service from a Wodby service manifest. Requires `confirm: true`. |
| `update_service_from_git` | Update a service from its Git source. Requires `confirm: true`. |
| `update_stack_from_git` | Update a stack from its Git source. Requires `confirm: true`. |

## Provisioning tools

These tools require `mcp:provision` when using OAuth and require `confirm: true`.

| Tool | Use |
| --- | --- |
| `create_cluster` | Create a managed cluster. Minimal input is prepared with defaults; unresolved integration, location, sizing, or billing choices are returned as questions. |
| `create_k3s_cluster` | Create a self-hosted k3s cluster record. |
| `create_wodby_cloud_cluster` | Create a Wodby Cloud cluster. If demo or sizing choices are unresolved, they are returned as questions. |
| `scale_cluster` | Scale a cluster node pool. |
| `create_app_from_stack` | Create an app and initial app environment from stack, environment, cluster, organization, and project names or IDs. Minimal input is prepared with defaults; unresolved deployment or service choices are returned as questions. |
| `create_app_instance_from_stack` | Create an app environment in an existing app. Minimal input is prepared with defaults; unresolved deployment or service choices are returned as questions. |
| `create_database` | Create a database. Password values are intentionally not accepted by this tool. |
| `create_database_db` | Create a DB inside a database. |
| `import_services` | Import services from a Git repository. |
| `import_stacks` | Import stacks from a Git repository. |
| `create_service_from_manifest` | Create a custom service from a Wodby service manifest. |
| `create_stack_from_manifest` | Create a custom stack from a Wodby stack manifest. |

## Sensitive tools

These tools require `mcp:sensitive` in addition to their other scope and require `confirm: true`.

| Tool | Use |
| --- | --- |
| `create_database_user` | Create a database user by submitting a password. The password is not returned in the MCP response. |

## Destructive tools

These tools require `mcp:destructive` when using OAuth and require `confirm: true`.

| Tool | Use |
| --- | --- |
| `create_import` | Import data into an app service or database DB. |
| `cancel_task` | Cancel a running task. |
| `delete_cluster` | Delete a cluster. |
| `delete_database` | Delete a database. |
| `delete_database_db` | Delete a DB inside a database. |
| `delete_database_user` | Delete a database user. |
| `update_app_instance_settings` | Update app environment settings such as automatic stack upgrades. |
| `update_stack_service` | Update selected stack-service settings. |
| `sync_stack_with_origin` | Sync a stack with its origin and optionally delete local configuration that no longer exists upstream. |
| `reconcile_app_instance_stack` | Reapply an app environment's assigned stack revision, optionally replace existing choices with stack defaults, and rebuild or redeploy all resulting services. |
| `upgrade_app_instance_stack` | Upgrade selected app environment stack sections. |
| `upgrade_cluster_infra` | Upgrade cluster infrastructure. |
| `upgrade_cluster_infra_apps` | Upgrade infrastructure app stacks for a cluster. |

MCP responses are compact summaries designed for AI agents. Some operation and task responses include `suggestedCalls`,
which are follow-up tool calls the client can use to continue the workflow, such as waiting for a build or deployment
task. Resource summaries omit secret-bearing values such as environment variable values, service tokens, registry
credentials, or integration credentials. Logs and container command output can still contain sensitive application data.
