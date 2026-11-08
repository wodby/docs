# MCP tools

Use the connected server's `tools/list` response for input schemas and currently available tools. Do not assume
an operation exists because a newer skill mentions it. See [MCP setup](../mcp.md) and the
[technical reference](reference.md) for connection and response handling.

Wodby MCP tools are grouped by scope. Most destructive and high-impact tools also require a `confirm: true` argument.
A tool marked "Takes no `confirm`" refuses that argument.

## Read tools

These tools require `mcp:read` when using OAuth.

| Tool | Use |
| --- | --- |
| `get_wodby_guidance` | Discover Wodby 2 workflow skills or load one by name. |
| `search_wodby_docs` | Search the public Wodby 2 documentation and return matching sections with the page to read. |
| `read_wodby_docs` | Read one page of the public Wodby 2 documentation as text, taken from `search_wodby_docs`. |
| `get_current_user` | Get the authenticated user, default organization, default projects, and available organizations. |
| `list_orgs` | List organizations available to the authenticated user. |
| `list_projects` | List projects in an organization by organization name or ID. |
| `list_envs` | List the [environment types](../../apps/environment-types.md) an app environment can have: `PROD`, `STAGING`, `TEST`, `DEV` and `FEATURE`. They are the same in every organization. |
| `list_integrations` | List integrations, optionally filtered by type, status, project, provider labels, or the environment type they are allowed in. Shows which integrations are outdated. |
| `get_integration_provider_upgrade` | Check whether an outdated integration can move to its provider's current revision, which fields the update would remove, and why an update is blocked. Requires `Modify/Delete` access to the integration. See [Integration provider updates](../../integrations/updates.md). |
| `list_apps` | List apps in an organization, optionally filtered by project names or IDs. |
| `show_app_status` | Return a dashboard-style app summary with app environments, services, latest build, latest deployment, operational needs, and follow-up suggestions for active tasks. |
| `get_app` | Get an app by ID. |
| `find_environment` | Find an app environment by organization, app name, and the legacy `instanceName` argument. |
| `list_app_environments` | List app environments with optional project, app, cluster, and status filters by names or IDs. |
| `get_workspace_context` | Read development workspace runtime, preview, setup and initial Git information. |
| `get_workspace_connection` | Get the owner’s SSH endpoint, fingerprint, the agents ready in the workspace and connection guidance. |
| `get_workspace_git_status` | Read the Git state of a workspace's checkout: branch, upstream, commits ahead and behind, the last commit, and the changed files. |
| `get_workspace_git_diff` | Read the uncommitted diff of one file in a workspace's checkout. A long diff is truncated; a binary file has none. |
| `get_app_environment` | Get an app environment by ID. |
| `get_app_preview_settings` | Get an app's [preview environment](../../apps/preview-environments.md) settings with the base environment and the services they seed. |
| `list_app_preview_pull_requests` | List the open pull requests an app can get a preview environment for, with the reason when one cannot. |
| `prepare_app_creation` | Resolve defaults and return missing questions for creating an app and initial app environment. This does not create anything. |
| `prepare_app_environment_creation` | Resolve defaults and return missing questions for creating an app environment in an existing app. This does not create anything. |
| `list_app_services` | List services for an app environment by app environment ID or the legacy organization/app/instance-name arguments. |
| `get_app_service` | Get an app service by ID. |
| `get_app_service_configuration` | Read how an app service is configured next to what its service allows: running and available versions, where its code is built from, settings, config file overrides, links, integrations, and volumes. Values of secret settings are not returned. |
| `get_service_guidance` | Read what the services of an app environment generate and wire for the application, such as settings files and connections to linked databases, caches, search, mail and file storage, and what the code still has to do. Also names the environment's stack and the address of its guide, when the stack has one. |
| `list_app_service_env_vars` | List an app service's environment variables and where each comes from: the app service, the service, the stack, a setting, a link or an integration. Secret values are not returned. |
| `get_app_service_resources` | Get an app service's replica count and each container's CPU and memory requests and limits. |
| `list_resource_presets` | List Wodby's resource presets and the organization's own, with their CPU and memory values. |
| `list_app_routes` | List an app environment's domains, the service and port each leads to, whether a certificate is attached, and whether the domain's DNS reaches the cluster. |
| `get_app_route_settings` | Read HTTP route settings such as HTTPS redirect, HSTS, request size, timeouts, and rate limits, for an environment's defaults or the values in effect for one domain. Available on clusters that use Envoy Gateway. |
| `list_app_ports` | List an app environment's service ports: protocol, internal number, whether the service marks it private, and the public port when it is published. |
| `list_app_auths` | List an app environment's HTTP basic authentication entries with their scope, username, and realm. Passwords are never returned. |
| `get_app_environment_access` | Read whether an app environment is Public or Protected, its Private App Access configuration, and the HTTP ports Private App Access endpoints can point at. |
| `get_app_access_provider_options` | Read what a Private App Access integration offers before you configure Private App Access with it: access types, scopes, hostnames, and required settings. |
| `list_app_environment_migrations` | List an app environment's moves to other clusters, newest first, with status, phase, failure message, when the retained source will be deleted, and the backup and restore of each data service. |
| `get_app_environment_stack_upgrade_changelog` | Preview what `upgrade_app_environment_stack` would change: stack versions and, per service, whether it is added, removed, or changes version, with release notes. An empty result means the environment already runs the newest revision. |
| `list_app_service_cron_schedules` | List cron schedules for an app environment or app service by IDs or by the legacy organization/app/instance-name/service arguments. |
| `list_app_builds` | List recent builds for an app environment by ID or the legacy organization/app/instance-name arguments. |
| `get_app_build` | Get an app build by ID. |
| `list_recent_deployments` | List recent deployments for an app environment by ID or the legacy organization/app/instance-name arguments. |
| `get_deployment` | Get deployment status, task, and service deployment details. |
| `get_task` | Get task jobs and steps, with follow-up suggestions when task results point to builds or deployments. |
| `wait_for_task` | Poll a task until it reaches a terminal state and optionally include bounded logs and follow-up suggestions. |
| `get_task_logs` | Get structured task job and step logs. |
| `get_task_step_logs` | Read a bounded page of live or historical task-step logs with sequence cursors. |
| `list_tasks` | List an organization's tasks, newest first, optionally by status or by the app, environment, cluster, database, stack, service or integration they belong to. |
| `diagnose_failed_deployment` | Inspect a deployment, find failed task steps, and return relevant log excerpts. |
| `list_clusters` | List clusters in an organization. |
| `get_cluster` | Get a cluster by ID. |
| `get_kubernetes_version_upgrade_plan` | Read a cluster's current Kubernetes version, the versions it can move to directly, and anything blocking the upgrade or worth a warning. |
| `get_cluster_infra_app_upgrade_changelog` | Preview what `upgrade_cluster_infra_apps` would change: per infrastructure app, the stack versions and per-service changes with release notes. |
| `list_cluster_component_updates` | List the updates Wodby can apply to single components of a cluster, such as Cilium on K3S or EKS add-ons, without a Kubernetes or infrastructure upgrade. Most components can't be updated this way, so the list is often empty. |
| `get_kubernetes_cluster_options` | Get provider-backed Kubernetes regions or zones, machine types, versions, and settings for a Kubernetes integration. |
| `get_wodby_cloud_options` | Get Wodby Cloud regions, machine types, pricing, and creation notes. |
| `prepare_cluster_creation` | Resolve defaults and return missing questions for creating managed, k3s, demo, or Wodby Cloud clusters. This does not create anything. |
| `get_cluster_metrics` | Get a current cluster metrics summary. |
| `list_cluster_node_metrics` | List node metrics for a cluster. |
| `list_databases` | List databases in an organization. |
| `get_database` | Get a database by ID. |
| `list_database_dbs` | List DBs inside a database. |
| `list_database_users` | List database users without returning passwords. |
| `get_database_options` | List the database types, versions, regions, and machine types a database integration offers, one choice at a time, to use with `create_database`. |
| `list_backups` | List backups of an app environment, app service, database or database DB, or of the whole organization, newest first, with where each is stored. |
| `list_backup_presets` | List backup presets, which save a backup destination and can run backups on a schedule. |
| `list_public_services` | List public service catalog items. |
| `list_services` | List services in an organization. |
| `get_service` | Get a service by name and optional revision number. |
| `get_service_contract` | Inspect revision-specific resolved service metadata; configuration values and source contents are omitted. Not an editable manifest. |
| `get_service_schema` | Get the Wodby service manifest JSON schema. |
| `get_service_examples` | Get concise Wodby service manifest examples. |
| `validate_service_manifest` | Validate a Wodby service manifest without creating it. |
| `list_git_repositories` | List the repositories a Git integration can read. |
| `check_git_access` | Check what a Git integration may do before relying on it: create a private repository, push to a repository, and open pull requests. Each check is allowed, denied with what to change in the Git provider, or unknown when the provider does not say. |
| `list_git_refs` | List a repository's branches and tags. |
| `list_git_files` | List the entries of one directory of a repository, without descending into it. |
| `read_git_file` | Read a text file of a repository, such as `composer.json`, `package.json`, a lock file, a Dockerfile or a manifest. |
| `validate_ci_files` | Validate a repository's Wodby CI files (`.wodby/pipeline.yml`, `.wodby/post-deployment.yml`) without running anything. |
| `list_providers` | List the integration providers an organization can use: its custom providers and Wodby's public ones, with their current revision and, for a provider from Git, its repository ref. |
| `get_provider_schema` | Get the Wodby custom provider manifest JSON schema. |
| `validate_provider_manifest` | Validate a Wodby custom provider manifest without creating it. |
| `list_public_stacks` | List public stack catalog items. |
| `list_stacks` | List stacks in an organization. |
| `get_stack` | Get a stack by name and optional revision number. |
| `get_stack_contract` | Inspect revision-specific stack composition, links, options, and service metadata without configuration values. Not an editable manifest. |
| `list_stack_services` | List the services of a stack in the revision your changes go to: its unpublished draft when it has one, including services you just added, otherwise the published revision. |
| `get_stack_service_configuration` | Read how a stack service is configured for the environments made from the stack, next to what its service allows: versions, settings, config files, CPU and memory, volume sizes, environment variables, cron schedules, links and integrations. Values of secret settings and secret variables are not returned. |
| `get_stack_origin_sync_changelog` | Preview what `sync_stack_with_origin` would bring: the origin's version and its release notes since this stack was copied. An empty result means there is nothing newer. |
| `get_stack_service_update_changelog` | Preview what `update_stack_service_revisions` would change: per outdated stack service, the current and new version with release notes. |
| `get_stack_schema` | Get the Wodby stack manifest JSON schema. |
| `get_stack_examples` | Get concise Wodby stack manifest examples. |
| `validate_stack_manifest` | Validate a Wodby stack manifest without creating it. |
| `get_app_service_pods` | Get Kubernetes pod status for an app service selected by ID or by service name with an app environment selector. |
| `get_app_service_logs` | Read bounded current or previous-container logs and return a log-access task ID. |
| `start_app_service_log_watch` | Open an audited, short-lived watch for new logs from one pod and container execution. |
| `read_app_service_log_watch` | Read cursor-based batches, including dropped-entry counts and watch status. |
| `stop_app_service_log_watch` | Stop a watch without changing the application. |
| `get_app_services_metrics` | Get current metrics for one or more app services selected by IDs or by service names with an app environment selector. |
| `get_app_environments_metrics` | Get current metrics for one or more app environments. |
| `list_wodby1_sources` | List what a Wodby 1 integration's token can migrate: its Wodby 1 organizations, or one organization's apps with their instances, and its servers. Needs organization owner or admin access, like the other Wodby 1 migration tools except `list_wodby1_migrations`. |
| `preview_wodby1_migration` | Preview migrating a Wodby 1 instance, app or server to Wodby 2: the plan, what it maps where, and every blocker and warning. It changes nothing on either platform. |
| `list_wodby1_migrations` | List an organization's latest Wodby 1 migrations with their status. |
| `get_wodby1_migration` | Show a Wodby 1 migration's status, its latest task, and what it waits for. |

## Operation tools

These tools require `mcp:operate` when using OAuth.

| Tool | Use |
| --- | --- |
| `prepare_workspace` | Rerun workspace setup, preserving the checkout. Requires `confirm: true`. |
| `start_workspace_agent_chat` | Hand a coding task to Wodby Agent in a development workspace, as a new chat there. Only the workspace owner can do this, and they follow the chat and answer its approvals in the workspace. With OAuth, also requires `mcp:exec`. Requires `confirm: true`. |
| `restart_workspace` | Restart the SSH runner, ending sessions; does not restart the application. Requires `confirm: true`. |
| `pause_workspace` | Pause a workspace environment. Requires `confirm: true`. |
| `resume_workspace` | Resume a paused workspace environment. Requires `confirm: true`. |
| `pull_workspace` | Bring a workspace's checkout up to date with its branch's upstream, then run the repository's post-deployment scripts unless you turn them off. Only the workspace owner can do this. The pull only fast-forwards: it refuses a branch with commits the upstream lacks, and leaves the checkout as it was when the pull would overwrite uncommitted changes. |
| `pause_app_environment` | Pause an app environment: its services stop and stop using compute, while its data and configuration are kept. The app is unreachable, and scheduled backups and cron jobs do not run, until it is resumed. |
| `resume_app_environment` | Resume a paused app environment. |
| `set_app_environment_maintenance_mode` | Turn an app environment's maintenance mode on or off. While it is on, visitors get a maintenance page with HTTP 503 instead of the app. |
| `create_deployment` | Create a deployment for one or more app services selected by IDs or by service names with an app environment selector, and suggest waiting for its task. |
| `redeploy_deployment` | Redeploy from an existing deployment. |
| `deploy_build` | Deploy a completed app build. |
| `create_builds` | Create builds for one or more app services selected by IDs or by service names with an app environment selector, and suggest waiting for the build task. |
| `run_app_service_action` | Run a named action on an app service selected by ID or by service name with an app environment selector. |
| `run_app_service_cron` | Run a cron schedule immediately by schedule ID or by schedule title with an app service selector. |
| `create_backup` | Create a backup for an app service or database DB. |
| `repeat_task` | Rerun an existing task. |
| `test_integration_permissions` | Check that an integration's credentials have the permissions its provider needs, for example after a failed cluster or database operation. Available for providers with a permission check, such as AWS, Google Cloud, Azure, and Cloudflare. Requires `Modify/Delete` access to the integration. |
| `retry_app_route_certificate` | Request a domain's Let's Encrypt certificate again, for example after fixing its DNS. A certificate is issued only once the domain's DNS reaches the cluster, so retrying before that fails again. |
| `retry_app_access_cleanup` | Repeat the cleanup left over from removed Private App Access, such as Cloudflare or Tailscale resources Wodby could not delete. The failed removal's task gives the cleanup ID. |
| `verify_wodby1_migration` | Once you have tested the migrated app on its technical domains and pointed DNS to Wodby 2, check DNS, configuration, imports, routes, certificates and workloads, and turn on the migrated cron schedules. A verified migration can no longer be rolled back. |

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
| `update_current_user` | Update the authenticated user's display name. |
| `create_project` | Create a project in an organization: a group of apps, clusters and other resources with its own members. Its machine name can't be changed later. |
| `enable_app_service` | Enable a disabled app service, together with the disabled services it requires. In a running environment this starts a deployment. |
| `disable_app_service` | Disable an app service: it stops and its domains and redirects are disabled, while its volumes are kept. Requires `confirm: true`. |
| `set_main_app_service` | Make an app service the main service of its environment, the one that serves the environment's root technical domain. Only an enabled service of the environment's own, with a public HTTP port, can be main. A stack upgrade makes the stack's main service the main one again. |
| `set_app_service_setting` | Set one of the settings an app service's service declares, such as a site name or an admin email. Secret settings are refused; set those in the dashboard. Running containers get the value with the next deployment of the service. |
| `set_app_service_env_var` | Add an environment variable to an app service, or change the one it already has with this name. It takes precedence over a variable with the same name from the service or the stack. Running containers get it with the next deployment of the service. |
| `delete_app_service_env_var` | Remove an environment variable set on an app service. A variable with the same name from the service or the stack then applies again. Variables that come from the service, the stack, settings or links can't be removed this way. Running containers lose it with the next deployment of the service. |
| `set_app_service_resources` | Change a container's CPU and memory requests and limits on an app service. Values you leave out stay as they are, and 0 removes a value so the service's default applies. A preset sets all four values at once, and values you give next to it override it. Running containers get the change with the next deployment of the service. |
| `set_app_service_replicas` | Change how many replicas of an app service run, at least one. Services that keep their data on one volume or can't run in parallel refuse more than one. Running replicas change with the next deployment of the service. |
| `create_app_service_cron_schedule` | Add a cron schedule to an app service: a command Wodby runs in the service on a five-field crontab in UTC. Schedules from the service or the stack already exist, so check `list_app_service_cron_schedules` first. |
| `update_app_service_cron_schedule` | Change a cron schedule of an app service, or turn it off and on. Settings you leave out stay as they are. |
| `set_app_service_config` | Override one of the config files an app service's service provides, such as `php.ini` or an nginx server block, or turn it off. The override replaces the whole file, so start from the current content. Running containers get it with the next deployment of the service. |
| `set_app_service_link` | Point one of an app service's links at another service of the same environment, such as a different database or cache, or remove an optional link. Running containers get the new connection settings with the next deployment of the service. |
| `add_app_service_integration` | Connect an organization integration, such as S3 storage or an SMTP relay, to an integration slot of an app service. Running containers get its settings with the next deployment of the service. |
| `remove_app_service_integration` | Detach an integration from an app service; the organization's integration itself stays. Features that rely on it, such as file uploads to S3 or sending mail, stop working with the next deployment of the service. |
| `rename_app` | Change the title an app is shown with. Its machine name, which names its Kubernetes resources and domains, never changes. |
| `rename_app_environment` | Change the title an app environment is shown with. Its machine name, which names its namespace and generated domains, never changes. |
| `update_cluster` | Update a cluster title. |
| `update_cluster_settings` | Update cluster settings such as automatic infrastructure upgrades. Requires `confirm: true`. |
| `update_k3s_cluster_public_ip` | Update the public IP for a self-hosted k3s cluster. Requires `confirm: true`. |
| `update_database` | Update a database title. |
| `update_database_user_dbs` | Update DB grants for a database user. Requires `confirm: true`. |
| `update_service_from_manifest` | Update an existing non-Git service from a Wodby service manifest. Requires `confirm: true`. |
| `update_service_from_git` | Update a service from its Git source. Requires `confirm: true`. |
| `create_git_repository` | Create a private repository under a Git integration you may modify, with a first commit holding a README. Not for a new app's code: creating an app that copies a boilerplate creates its repository. Refused on Bitbucket, where you create the repository yourself. |
| `create_git_branch` | Create a branch at the head of another branch, through a Git integration you may modify. It never moves or replaces an existing branch. |
| `create_git_pull_request` | Open a pull request (a merge request on GitLab) from one branch of a repository into another, through a Git integration you may modify. It never merges anything. |
| `close_git_pull_request` | Close an open pull request (a merge request on GitLab) without merging it, through a Git integration you may modify. It never deletes a branch. On Bitbucket the pull request is declined, which can't be undone; on GitHub and GitLab you can reopen it there. |
| `commit_git_files` | Add or replace text files in a repository with one commit on a branch, through a Git integration you may modify. It never deletes files, rewrites history or creates a branch, and fails instead of overwriting when the branch moved meanwhile. A file you send replaces the whole file. Builds and deployments that follow the branch can start from the commit. |
| `create_workspace_pull_request` | Open a pull request (a merge request on GitLab) from a development workspace's branch in the repository its code comes from. Push the branch with Git first. Only the workspace owner can do this. |
| `update_provider_from_manifest` | Publish a new revision of a custom provider that does not come from Git. Existing integrations stay on their revision until you upgrade them in the dashboard. Requires `confirm: true`. |
| `update_provider_from_git` | Update a custom provider from its Git repository at a branch, tag, or commit. Existing integrations stay on their revision until you upgrade them in the dashboard. Requires `confirm: true`. |
| `update_stack_from_git` | Update a stack from its Git source. Requires `confirm: true`. |
| `add_stack_service` | Add a service, such as Redis or Solr, to a stack your organization owns. The addition is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `set_stack_service_link` | Point one of a stack service's links at another service of the same stack, such as PHP's cache link at a newly added Redis, or remove an optional link. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `set_stack_service_config` | Override one of the config files a stack service's service provides, such as `php.ini`. The override replaces the whole file, so start from the content `get_stack_service_configuration` shows. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `set_stack_service_resources` | Change the CPU and memory requests and limits a stack service's container gets, or apply a preset from `list_resource_presets`. Values you leave out stay as they are. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `set_stack_service_setting` | Set or remove the value a stack service gives one of its service's settings, such as a site name. Secret settings are refused; set those in the dashboard. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `set_stack_service_volume` | Set the size, in GB, of one of a stack service's volumes, or return it to the service's default. Existing volumes keep their size. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `update_stack_service_options` | Choose which versions of its service a stack service offers and which one new environments get by default. Existing environments keep the version they run. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `set_stack_service_env_var` | Add an environment variable a stack service gives the environments made from the stack, or change the one it already sets. It can apply to one container and to one environment type. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `delete_stack_service_env_var` | Remove an environment variable a stack service sets. Variables the service itself declares can't be removed this way. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `create_stack_service_cron_schedule` | Add a cron schedule a stack service gives the environments made from the stack: a command Wodby runs in the service on a five-field crontab in UTC. Running schedules can need a paid subscription. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `update_stack_service_cron_schedule` | Change a stack service's cron schedule, or turn it off and on. Settings you leave out stay as they are. The change is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `ignore_stack_service_revision` | Stop offering one service revision as an update for a stack service and its derivatives. The next newer revision of the service is offered again. |
| `create_app_route` | Add a domain to an app environment, routed to a port of an app service. By default Wodby requests a Let's Encrypt certificate, issued once the domain's DNS points to the cluster. |
| `update_app_route` | Change a route: turn it off or on, make it the primary domain, change its path or certificate, or redirect it to another host. Generated and private routes can't be changed. |
| `set_app_route_setting` | Set one HTTP route setting, such as HTTPS redirect, HSTS, request size, timeouts, or rate limits, as an environment default or for one domain. Wodby applies it with a routing deployment. Available on clusters that use Envoy Gateway. |
| `remove_app_route_setting` | Remove an HTTP route setting from an environment's defaults or from one domain, so the next layer's value applies again: a domain falls back to the service's and then the environment's default. |
| `unpublish_app_port` | Stop exposing a published port to the internet. Clients outside the cluster that use it, such as SSH or a remote database client, lose access. |
| `create_backup_preset` | Create a backup preset: a saved destination that by default also runs backups every day in a time window. Presets need a paid subscription. |
| `update_backup_preset` | Change a backup preset's destination or schedule. Settings you leave out stay as they are. The change applies to backups made afterward; existing backups stay where they are. |
| `create_app_auth` | Put HTTP basic authentication in front of an app environment, some of its services, or one domain, or exempt services or a domain from it. The password is generated and never returned here; reveal it on the environment's **Domains > Auths** page in the dashboard. |
| `update_app_auth` | Change a basic auth entry's username, realm, or scope, or replace its password with a newly generated one, which you reveal in the dashboard. |
| `update_app_service` | Change the version an app service runs or where its code is built from, such as another branch. The result says whether the service needs a new build or only a deployment. A database's major version change can need a data migration. |
| `update_app_environment_cicd_settings` | Choose the CI provider that builds an app environment's services and the container registry for their images. This applies to future builds; existing builds keep what they were built with. |

## Provisioning tools

These tools require `mcp:provision` when using OAuth and require `confirm: true`, except where a tool takes no `confirm`.

| Tool | Use |
| --- | --- |
| `create_cluster` | Create a managed cluster. Minimal input is prepared with defaults; unresolved integration, location, sizing, or billing choices are returned as questions. |
| `create_k3s_cluster` | Create a self-hosted k3s cluster record. |
| `create_wodby_cloud_cluster` | Create a Wodby Cloud cluster. If demo or sizing choices are unresolved, they are returned as questions. |
| `scale_cluster` | Scale a cluster node pool. |
| `update_cluster_gpu_node_pool` | Add, resize, replace or remove a cluster's [GPU node pool](../../clusters/gpu.md), which adds or removes paid compute capacity. Removal is refused while pods request GPUs. Changing the machine type creates the new pool before deleting the old one. |
| `create_app_from_stack` | Create an app and initial app environment from stack, cluster, organization, and project names or IDs. Choose the environment type with `environment_type`; it defaults to `DEV`. Minimal input is prepared with defaults; unresolved deployment or service choices are returned as questions. |
| `create_app_environment_from_stack` | Create an app environment in an existing app. Choose its environment type with `environment_type`; it defaults to `DEV`. Minimal input is prepared with defaults; unresolved deployment or service choices are returned as questions. |
| `add_app_service_volume` | Add one of the optional volumes an app service's service declares and the environment does not have yet. A volume is billable storage in the cluster. Volumes that already exist can't be resized or removed with this tool. |
| `create_app_preview_environment` | Create a preview environment for an open pull request. |
| `create_database` | Create a database for one environment type, set with `environment_type`. Password values are intentionally not accepted by this tool. |
| `create_database_db` | Create a DB inside a database. |
| `import_services` | Import services from a Git repository. |
| `import_stacks` | Import stacks from a Git repository. |
| `create_service_from_manifest` | Create a custom service from a Wodby service manifest. |
| `create_stack_from_manifest` | Create a custom stack from a Wodby stack manifest. |
| `create_provider_from_manifest` | Create a custom integration provider from a provider manifest. Create its integrations and enter their credentials in the dashboard. |
| `import_providers` | Import custom integration providers from a Git repository: `provider.yml` at its root, or the providers an `index.yml` lists. |
| `duplicate_stack` | Duplicate a stack into an organization and optional project. Takes no `confirm`. |
| `start_wodby1_migration` | Run a previewed Wodby 1 migration as a background task, which can take an hour: create the Wodby 2 app and its environments, configure, build and deploy them, and import the data. Pass the arguments of `preview_wodby1_migration` and its `planHash`; only that plan is applied. Public traffic stays on Wodby 1 until you change DNS. Takes no `confirm`. |
| `resume_wodby1_migration` | Continue a paused or stopped Wodby 1 migration from where it stopped. Completed work is reused. To change its choices, use `restart_wodby1_migration` instead. Takes no `confirm`. |

## Sensitive tools

These tools require `mcp:sensitive` in addition to their other scope.

| Tool | Use |
| --- | --- |
| `create_database_user` | Create a database user by submitting a password. The password is not returned in the MCP response. Requires `mcp:provision` and `confirm: true`. |
| `get_backup_download` | Get a time-limited download link for a backup's file. Requires `mcp:read`. Anyone with the link can download the backup, which can contain your database and files, until it expires. Share it only with the person who asked for it, and do not store or repost it. |

## Destructive tools

These tools require `mcp:destructive` when using OAuth and require `confirm: true`, except where a tool takes no `confirm`.

| Tool | Use |
| --- | --- |
| `create_import` | Import data into an app service or database DB. |
| `cancel_task` | Cancel a running task. |
| `cancel_deployment` | Cancel a deployment that has not started rolling out, such as one waiting for a build in an external CI system. To stop a deployment that is already rolling out, use `cancel_task`. |
| `delete_cluster` | Delete a cluster. |
| `delete_app` | Delete an app. Its app environments, their services, data and routes go with it. |
| `delete_app_environment` | Delete an app environment with its services, data and routes. With `force`, it is removed from Wodby even when its Kubernetes resources can't be deleted, for example because its cluster is gone; use that only when an ordinary deletion failed, because resources left on a reachable cluster then need removing by hand. |
| `delete_app_service_cron_schedule` | Delete a cron schedule of an app service, so its command no longer runs. To stop it for a while, turn it off with `update_app_service_cron_schedule` instead. |
| `delete_stack_service_cron_schedule` | Remove a cron schedule a stack service adds. To stop it for a while, turn it off with `update_stack_service_cron_schedule` instead. The removal is saved to the stack's draft and reaches environments after `publish_stack_draft` and an upgrade. |
| `delete_stack` | Delete a stack of the organization. A stack that app environments still use can't be deleted. |
| `delete_service` | Delete a custom service of the organization. A service that stacks still use can't be deleted. |
| `delete_integration` | Delete an integration and the credentials it holds. Clusters, apps and stacks that use it lose access to that account. |
| `upgrade_integration_provider_revision` | Update an outdated integration to its provider's current revision after `get_integration_provider_upgrade` shows it can be updated. With `drop_removed_fields`, the update permanently deletes the stored values of fields the new revision removes, and the app services that use them are marked for redeploy. An integration shared with your organization is updated by its owner. |
| `delete_backup_preset` | Delete a backup preset, so its scheduled backups stop. Backups it already made are kept. |
| `delete_app_route` | Remove a route from an app environment, so its domain stops reaching the app. To stop serving a domain for a while, turn it off with `update_app_route` instead. |
| `publish_app_port` | Make a non-HTTP port, such as SSH or a database's TCP port, reachable from the internet on a public port Wodby assigns. Anyone on the internet can then reach it, so publish only what has its own authentication, and prefer a private network for databases. Private and HTTP ports can't be published. Publishing may redeploy the cluster's gateway first. |
| `create_app_access` | Make an app environment Protected by publishing it through a Private App Access integration or a private network. Public routes in the scope stop serving visitors at once. The access type can't be changed later. Requires a paid subscription. |
| `update_app_access` | Change an app environment's Private App Access scope, provider settings, or endpoints. Routes leaving the scope become public, and routes entering it stop serving the public. |
| `delete_app_access` | Make an app environment Public again: remove its Private App Access, delete the provider's resources, and restore its public routes, which anyone can then reach. |
| `delete_app_auth` | Remove a basic auth entry. What it protected becomes reachable without a password, unless a broader entry still covers it. |
| `delete_database` | Delete a database. |
| `delete_database_db` | Delete a DB inside a database. |
| `delete_database_user` | Delete a database user. |
| `update_app_environment_settings` | Update app environment settings such as automatic stack upgrades and build-image cleanup. |
| `update_app_preview_settings` | Update an app's preview environment settings. Only the given settings change. |
| `update_stack_service` | Update selected stack-service settings. |
| `update_stack_service_revisions` | Move a stack's services to the newest revisions of their services. Pinned services and ignored revisions stay as they are. Environments then move to the new stack revision with `upgrade_app_environment_stack`. |
| `update_stack_from_manifest` | Replace the composition of a stack that does not come from Git with a complete stack manifest. Services the manifest leaves out are removed from the stack. |
| `remove_stack_service` | Remove a service and its derivatives from a stack your organization owns. A required service, or one other services require through a link, is refused. The removal is saved to the stack's draft and reaches environments only after `publish_stack_draft` and an upgrade. A stack that comes from Git is changed in its repository instead. |
| `publish_stack_draft` | Publish a stack's unpublished draft as its new revision. Publishing checks the main service and required links and changes nothing when they fail. Environments then move to the new revision with `upgrade_app_environment_stack`, or on their own where automatic stack upgrades are on. |
| `discard_stack_draft` | Discard a stack's unpublished draft and every change saved to it. The published revision and the app environments on it stay as they are. |
| `sync_stack_with_origin` | Sync a stack with its origin and optionally delete local configuration that no longer exists upstream. |
| `reconcile_app_environment_stack` | Reapply an app environment's assigned stack revision, optionally replace existing choices with stack defaults, and rebuild or redeploy all resulting services. |
| `upgrade_app_environment_stack` | Upgrade an app environment to its latest stack revision. Preview it first with `get_app_environment_stack_upgrade_changelog`. Optional settings can replace your existing choices with stack defaults, and the environment's main service always follows the stack. |
| `migrate_app_environment` | Move an app environment and its persistent data to another cluster of the organization. The environment is unavailable while its data is backed up, restored on the target and deployed, so plan a maintenance window. The environment must be OK with an active deployment and not in maintenance mode, without Private App Access, private or custom routes, or published TCP/UDP ports. Both clusters must be OK, every data service needs backup and import operations, every built service an active build, and the final backups use Wodby Blob Storage, which needs a paid subscription. Wodby keeps the stopped source for seven days. |
| `rollback_app_environment_migration` | Restore an app environment on its source cluster after a migration that failed and whose automatic recovery did not finish. Fix the underlying cluster, storage, or deployment problem first. A completed migration can't be rolled back. |
| `cleanup_app_environment_migration` | Permanently delete the stopped source an app environment left on its old cluster after a completed migration, before the seven-day retention ends. The migration backups stay. |
| `upgrade_cluster_infra` | Upgrade cluster infrastructure. |
| `upgrade_cluster_infra_apps` | Upgrade infrastructure app stacks for a cluster. |
| `update_cluster_component` | Apply one update that `list_cluster_component_updates` lists. Read the update's note first, then follow the task for the result. |
| `upgrade_kubernetes_version` | Upgrade a cluster's Kubernetes to a version `get_kubernetes_version_upgrade_plan` lists. The provider can rotate control-plane components and worker nodes, and the Kubernetes API can be briefly unavailable, so run it for production in a maintenance window. It can't be undone. Supported for EKS, AKS, GKE Standard, DigitalOcean, OVH, and K3S clusters; Wodby Cloud and serverless clusters are refused. |
| `recycle_cluster_nodes` | Refresh a managed cluster's worker nodes. EKS moves each node group to its latest node image and leaves a group that already runs it in place; AKS and DigitalOcean replace every node. Workloads move to the new nodes, so applications restart, and new deployments wait until it ends. The cluster must be in OK status with no active application operations. GKE, OVHcloud, Wodby Cloud, serverless, and single-node clusters are refused. |
| `restart_wodby1_migration` | Start a Wodby 1 migration over with a new preview's choices: first delete what the migration created in Wodby 2, including its imported data, then apply the new plan. Apps and integrations that existed before stay, and so does the cluster. Preview again first and pass that preview's `planHash`. Takes no `confirm`. |
| `rollback_wodby1_migration` | Delete the Wodby 2 resources a migration created, including its imported data. Apps and resources that existed before stay, and Wodby 1 isn't touched. Refused once the migration is verified. Takes no `confirm`. |

MCP responses are compact summaries designed for AI agents. Some operation and task responses include `suggestedCalls`,
which are follow-up tool calls the client can use to continue the workflow, such as waiting for a build or deployment
task. Resource summaries omit secret-bearing values such as environment variable values, service tokens, registry
credentials, or integration credentials. Logs and container command output can still contain sensitive application data.
