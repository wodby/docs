# Wodby MCP

Wodby exposes a Model Context Protocol (MCP) server for AI assistants and coding agents that need Wodby context.

Use MCP when you want an AI client to inspect Wodby resources, summarize app and deployment state, create or operate
apps, or diagnose failed operations without manually copying IDs, task logs, and deployment details between tools.

## Endpoint

Use the hosted Wodby MCP endpoint:

```text
https://mcp.wodby.com/mcp
```

The endpoint uses Streamable HTTP. Clients must send MCP JSON-RPC requests over `POST`.

## Authentication

The recommended setup uses MCP OAuth. When your MCP client connects, Wodby opens a browser-based authorization flow in
the Dashboard. Sign in, choose the organization to grant, and approve the requested MCP scopes.

Wodby currently exposes these MCP OAuth scopes:

- `mcp:read` for discovery, diagnostics, deployment status, task status, bounded metrics, pod status, and logs.
- `mcp:operate` for task-backed operations such as deployments, builds, backups, cron runs, app service actions, and
  task repeats.
- `mcp:configure` for settings, metadata, stack configuration, and resource configuration.
- `mcp:provision` for creating infrastructure and resource objects.
- `mcp:destructive` for deletes, cancellations, destructive imports, and high-impact upgrades.
- `mcp:sensitive` for submitting secret or credential values. Sensitive values are not returned in MCP responses.

Default OAuth grants request all scopes except `mcp:sensitive`. Tools that use sensitive input, such as database user
passwords, require a client to explicitly request `mcp:sensitive`.

OAuth grants are organization-scoped and run with the permissions of the Wodby user who approved them.

You can also authenticate manually with a Wodby [API key](api-keys.md) sent as the `X-API-KEY` header.

Create an API key from [User settings > API keys](../user/api-keys.md). Each key belongs to one organization and runs
with the permissions of the user who created it.

Set the key in your shell:

```bash
export WODBY_API_KEY=...
```

## Client configuration

For MCP clients that run local server commands, use `mcp-remote` without custom headers. It discovers Wodby's OAuth
metadata, opens the browser flow, and stores the returned MCP token locally:

```json
{
  "mcpServers": {
    "wodby": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.wodby.com/mcp"
      ]
    }
  }
}
```

Restart your MCP client after changing its configuration.

For clients or scripts that cannot complete OAuth, keep using `X-API-KEY`:

```json
{
  "mcpServers": {
    "wodby": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.wodby.com/mcp",
        "--header",
        "X-API-KEY: ${WODBY_API_KEY}"
      ]
    }
  }
}
```

### Claude Desktop

Open the Claude Desktop MCP configuration file and add the Wodby server:

=== "macOS"

    ```bash
    code ~/Library/Application\ Support/Claude/claude_desktop_config.json
    ```

=== "Windows"

    ```powershell
    code "$env:APPDATA\Claude\claude_desktop_config.json"
    ```

```json
{
  "mcpServers": {
    "wodby": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.wodby.com/mcp"
      ]
    }
  }
}
```

Save the file, restart Claude Desktop, and approve the Wodby browser authorization when prompted.

### Claude Code

Claude Code can connect to remote HTTP MCP servers directly:

```bash
claude mcp add --transport http wodby https://mcp.wodby.com/mcp
```

Then run the OAuth login flow:

```bash
claude mcp login wodby
```

### Codex

Codex can add Wodby from the CLI:

```bash
codex mcp add wodby --url https://mcp.wodby.com/mcp
```

If Codex does not open the authorization flow during add, run:

```bash
codex mcp login wodby
```

Codex stores MCP servers in `~/.codex/config.toml`, or in `.codex/config.toml` for a trusted project. The equivalent
manual configuration is:

```toml
[mcp_servers.wodby]
url = "https://mcp.wodby.com/mcp"
```

In the Codex terminal UI, use `/mcp` to check connected MCP servers.

To use a manual API key instead of OAuth, configure `env_http_headers`:

```toml
[mcp_servers.wodby]
url = "https://mcp.wodby.com/mcp"
env_http_headers = { "X-API-KEY" = "WODBY_API_KEY" }
```

Set the key before starting Codex:

```bash
export WODBY_API_KEY=...
codex
```

## Using Wodby in your MCP client

After the server is connected, start a normal chat in your MCP client. In most clients, you do not call MCP tool names
directly. Ask for the Wodby information or action you want, and the client chooses the matching Wodby tool calls.

For Claude Code, start a chat after adding and logging in to the server:

```bash
claude
```

For Codex, start the terminal UI after adding and logging in to the server:

```bash
codex
```

In Codex, run `/mcp` to verify that `wodby` is connected. If the assistant does not use Wodby automatically, name the
server in the prompt:

```text
Use Wodby to list my organizations and projects.
```

A practical workflow is:

1. Start with names where possible: organization, project, app, app instance, app service, cluster, stack, and
   environment names are easier for an assistant to use than numeric IDs.
2. Ask for a read-only summary or diagnosis before making changes.
3. Ask the assistant to explain the intended operation.
4. Approve the Wodby tool call in your client when you are ready to run it.

Many tools still accept IDs when you have them. For app workflows, MCP tools can usually resolve common selectors such
as `org`, `project`, `app`, `instance`, `app_service`, `cluster`, `environment`, and `stack`.

### Discovery examples

```text
Use Wodby to list my organizations and projects.
```

```text
Use Wodby to show the status of app example in organization acme.
```

```text
Find the production instance for app example in organization acme.
```

```text
List app instances in project storefront that are not deployed or have a failed latest deployment.
```

```text
List services for the production instance of app example in organization acme.
```

### Diagnostics examples

```text
Use Wodby to explain why deployment 789 failed and include the failed task step logs.
```

```text
Show pods and current service metrics for the php service in the production instance of app example, then summarize anything unhealthy.
```

```text
Check the latest builds and deployments for the production instance of app example and tell me what changed most recently.
```

### Operation examples

```text
Create builds for the php and node app services in the production instance of app example, then show the task status.
```

```text
Create a deployment for the php and nginx app services in the production instance of app example, then wait for the task and include logs if it fails.
```

```text
Run the clear-cache action on the php app service in the production instance of app example.
```

```text
Run cron schedule 123 and follow the created task until it finishes.
```

```text
Create a backup for database DB db-abc before the next deployment.
```

### Cluster, database, and catalog examples

```text
List clusters in org 123, summarize node health, and recommend whether cluster cluster-abc needs scaling.
```

```text
Scale cluster cluster-abc to min 2 and max 5 nodes. Explain the change first, then use confirm=true if I approve.
```

```text
Import services from Git repository repo-abc on branch main. Show the import target before using confirm=true.
```

```text
Create database DB app_prod inside database db-abc. Ask before using confirm=true.
```

```text
Create an app named example from stack drupal11 in organization acme, environment production, and cluster main. Explain the resolved inputs before using confirm=true.
```

### Service and stack manifest examples

Wodby MCP can help an assistant draft, validate, and create custom Wodby services and stacks from manifests. Ask the
assistant to fetch the Wodby schema and examples first, validate the generated manifest, and show you the result before
creating it. Creation requires `confirm: true`.

```text
Generate a Wodby service manifest for this Helm chart URL, validate it with Wodby, and show the manifest before creating it in org 123.
```

```text
Create a Wodby stack manifest that uses service my-service and validates against the Wodby stack schema. Ask before using confirm=true.
```

### Sensitive and destructive examples

Sensitive actions, such as creating a database user with a password, require the `mcp:sensitive` OAuth scope. Destructive
and other high-impact actions require `confirm: true` in the tool call.

```text
Create database user app_rw for database db-abc with grants to DB app_prod. Request the password from me first and do not print it back.
```

```text
Delete database DB old_test from database db-abc. Show exactly what will be deleted and ask me before using confirm=true.
```

## Available tools

Wodby MCP tools are grouped by scope. Destructive and high-impact tools also require a `confirm: true` argument.

### Read tools

These tools require `mcp:read` when using OAuth.

| Tool | Use |
| --- | --- |
| `get_current_user` | Get the authenticated user, default organization, default projects, and available organizations. |
| `list_orgs` | List organizations available to the authenticated user. |
| `list_projects` | List projects in an organization by organization name or ID. |
| `list_apps` | List apps in an organization, optionally filtered by project names or IDs. |
| `show_app_status` | Return a dashboard-style app summary with instances, services, latest build, latest deployment, and operational needs. |
| `get_app` | Get an app by ID. |
| `find_environment` | Find an app instance by organization, app name, and instance name. |
| `list_app_instances` | List app instances with optional project, app, cluster, and status filters by names or IDs. |
| `get_app_instance` | Get an app instance by ID. |
| `list_app_services` | List services for an app instance by app instance ID or organization/app/instance names. |
| `get_app_service` | Get an app service by ID. |
| `list_app_builds` | List recent builds for an app instance. |
| `get_app_build` | Get an app build by ID. |
| `list_recent_deployments` | List recent deployments for an app instance. |
| `get_deployment` | Get deployment status, task, and service deployment details. |
| `get_task` | Get task jobs and steps. |
| `wait_for_task` | Poll a task until it reaches a terminal state and optionally include bounded logs. |
| `get_task_logs` | Get structured task job and step logs. |
| `get_task_step_logs` | Get recent inline logs for a task step. |
| `diagnose_failed_deployment` | Inspect a deployment, find failed task steps, and return relevant log excerpts. |
| `list_clusters` | List clusters in an organization. |
| `get_cluster` | Get a cluster by ID. |
| `get_cluster_metrics` | Get a current cluster metrics summary. |
| `list_cluster_node_metrics` | List node metrics for a cluster. |
| `list_databases` | List databases in an organization. |
| `get_database` | Get a database by ID. |
| `list_database_dbs` | List DBs inside a database. |
| `list_database_users` | List database users without returning passwords. |
| `list_public_services` | List public service catalog items. |
| `list_services` | List services in an organization. |
| `get_service` | Get a service by name and optional revision number. |
| `get_service_schema` | Get the Wodby service manifest JSON schema. |
| `get_service_examples` | Get concise Wodby service manifest examples. |
| `validate_service_manifest` | Validate a Wodby service manifest without creating it. |
| `list_public_stacks` | List public stack catalog items. |
| `list_stacks` | List stacks in an organization. |
| `get_stack` | Get a stack by name and optional revision number. |
| `get_stack_schema` | Get the Wodby stack manifest JSON schema. |
| `get_stack_examples` | Get concise Wodby stack manifest examples. |
| `validate_stack_manifest` | Validate a Wodby stack manifest without creating it. |
| `get_app_service_pods` | Get Kubernetes pod status for an app service. |
| `get_app_services_metrics` | Get current metrics for one or more app services. |
| `get_app_instances_metrics` | Get current metrics for one or more app instances. |

### Operation tools

These tools require `mcp:operate` when using OAuth.

| Tool | Use |
| --- | --- |
| `create_deployment` | Create a deployment for one or more app services selected by IDs or by service names with an app instance selector. |
| `redeploy_deployment` | Redeploy from an existing deployment. |
| `deploy_build` | Deploy a completed app build. |
| `create_builds` | Create builds for one or more app services selected by IDs or by service names with an app instance selector. |
| `run_app_service_action` | Run a named action on an app service selected by ID or by service name with an app instance selector. |
| `run_app_service_cron` | Run a cron schedule immediately. |
| `create_backup` | Create a backup for an app service or database DB. |
| `repeat_task` | Rerun an existing task. |
| `update_current_user` | Update the authenticated user's display name. |
| `duplicate_stack` | Duplicate a stack into an organization and optional project. |

### Configuration tools

These tools require `mcp:configure` when using OAuth. Tools marked here with `confirm: true` make high-impact
configuration changes.

| Tool | Use |
| --- | --- |
| `update_cluster` | Update a cluster title. |
| `update_cluster_settings` | Update cluster settings such as automatic infrastructure upgrades. Requires `confirm: true`. |
| `update_k3s_cluster_public_ip` | Update the public IP for a self-hosted k3s cluster. Requires `confirm: true`. |
| `update_database` | Update a database title. |
| `update_database_user_dbs` | Update DB grants for a database user. Requires `confirm: true`. |
| `update_service_from_git` | Update a service from its Git source. Requires `confirm: true`. |
| `update_stack_from_git` | Update a stack from its Git source. Requires `confirm: true`. |

### Provisioning tools

These tools require `mcp:provision` when using OAuth and require `confirm: true`.

| Tool | Use |
| --- | --- |
| `create_cluster` | Create a managed cluster. |
| `create_k3s_cluster` | Create a self-hosted k3s cluster record. |
| `create_wodby_cloud_cluster` | Create a Wodby Cloud cluster. |
| `scale_cluster` | Scale a cluster node pool. |
| `create_app_from_stack` | Create an app and initial app instance from stack, environment, cluster, organization, and project names or IDs. |
| `create_database` | Create a database. Password values are intentionally not accepted by this tool. |
| `create_database_db` | Create a DB inside a database. |
| `import_services` | Import services from a Git repository. |
| `import_stacks` | Import stacks from a Git repository. |
| `create_service_from_manifest` | Create a custom service from a Wodby service manifest. |
| `create_stack_from_manifest` | Create a custom stack from a Wodby stack manifest. |

### Sensitive tools

These tools require `mcp:sensitive` in addition to their other scope and require `confirm: true`.

| Tool | Use |
| --- | --- |
| `create_database_user` | Create a database user by submitting a password. The password is not returned in the MCP response. |

### Destructive tools

These tools require `mcp:destructive` when using OAuth and require `confirm: true`.

| Tool | Use |
| --- | --- |
| `create_import` | Import data into an app service or database DB. |
| `cancel_task` | Cancel a running task. |
| `delete_cluster` | Delete a cluster. |
| `delete_database` | Delete a database. |
| `delete_database_db` | Delete a DB inside a database. |
| `delete_database_user` | Delete a database user. |
| `update_app_instance_settings` | Update app-instance settings such as automatic stack upgrades. |
| `update_stack_service` | Update selected stack-service settings. |
| `sync_stack_with_origin` | Sync a stack with its origin and optionally delete local configuration that no longer exists upstream. |
| `upgrade_app_instance_stack` | Upgrade selected app-instance stack sections. |
| `upgrade_cluster_infra` | Upgrade cluster infrastructure. |
| `upgrade_cluster_infra_apps` | Upgrade infrastructure app stacks for a cluster. |

MCP responses are compact summaries designed for AI agents. They do not expose secret-bearing values such as
environment variable values, service tokens, registry credentials, or integration credentials.

## Choosing MCP, API, SDKs, or CLI

- Use [MCP](mcp.md) when an AI assistant needs Wodby context or diagnostics.
- Use the [REST API](api.md) for direct resource automation and OpenAPI-based tooling.
- Use [SDKs](sdks.md) when you want generated models and request helpers.
- Use the [Wodby CLI](cli.md) for CI build, release, deploy, and shell workflows.

## Troubleshooting

If the MCP server returns `401 Unauthorized` during OAuth setup, run your client's MCP login command again and approve
the Wodby authorization in the browser.

If you use API-key authentication, check that `WODBY_API_KEY` is set in the environment available to your MCP client
process.

If an AI client can list tools but tool calls return access errors, verify that the OAuth grant or API key belongs to
the organization you are querying and that the approving user can view the requested project, app, task, or deployment.

If the browser authorization does not open, verify that the MCP client supports remote MCP OAuth. Use `mcp-remote` or
the API-key header fallback when the client does not support OAuth directly.

## Related pages

- [API keys](api-keys.md)
- [Wodby API](api.md)
- [Wodby CLI](cli.md)
- [Tasks](../tasks.md)
- [Deploys](../apps/deploys.md)
