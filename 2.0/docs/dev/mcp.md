# Wodby MCP

Wodby exposes a Model Context Protocol (MCP) server for AI assistants and coding agents that need Wodby context.

Use MCP when you want an AI client to inspect Wodby resources, summarize deployment state, or diagnose failed
operations without manually copying IDs, task logs, and deployment details between tools.

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

## Available tools

Wodby MCP tools are grouped by scope. Destructive and high-impact tools also require a `confirm: true` argument.

### Read tools

These tools require `mcp:read` when using OAuth.

| Tool | Use |
| --- | --- |
| `get_current_user` | Get the authenticated user, default organization, default projects, and available organizations. |
| `list_orgs` | List organizations available to the authenticated user. |
| `list_projects` | List projects in an organization. |
| `list_apps` | List apps in an organization, optionally filtered by project. |
| `get_app` | Get an app by ID. |
| `find_environment` | Find an app instance by organization, app name, and instance name. |
| `list_app_instances` | List app instances with optional project, app, cluster, and status filters. |
| `get_app_instance` | Get an app instance by ID. |
| `list_app_services` | List services for an app instance. |
| `get_app_service` | Get an app service by ID. |
| `list_app_builds` | List recent builds for an app instance. |
| `get_app_build` | Get an app build by ID. |
| `list_recent_deployments` | List recent deployments for an app instance. |
| `get_deployment` | Get deployment status, task, and service deployment details. |
| `get_task` | Get task jobs and steps. |
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
| `list_public_stacks` | List public stack catalog items. |
| `list_stacks` | List stacks in an organization. |
| `get_stack` | Get a stack by name and optional revision number. |
| `get_app_service_pods` | Get Kubernetes pod status for an app service. |
| `get_app_services_metrics` | Get current metrics for one or more app services. |
| `get_app_instances_metrics` | Get current metrics for one or more app instances. |

### Operation tools

These tools require `mcp:operate` when using OAuth.

| Tool | Use |
| --- | --- |
| `create_deployment` | Create a deployment for one or more app services. |
| `redeploy_deployment` | Redeploy from an existing deployment. |
| `deploy_build` | Deploy a completed app build. |
| `create_builds` | Create builds for one or more app services. |
| `run_app_service_action` | Run a named action on an app service. |
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
| `create_database` | Create a database. Password values are intentionally not accepted by this tool. |
| `create_database_db` | Create a DB inside a database. |
| `import_services` | Import services from a Git repository. |
| `import_stacks` | Import stacks from a Git repository. |

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

## Example prompts

After connecting the MCP server, ask your AI client questions such as:

- `List my Wodby organizations.`
- `Find the production instance for app example in org 123.`
- `Show recent deployments for app instance 456.`
- `Why did deployment 789 fail?`
- `Get logs for the failed task step.`
- `List services in app instance 456 and summarize which ones need redeploy.`
- `Create a build for app service 456.`
- `Redeploy deployment 789.`
- `Run cron schedule 123.`
- `List clusters in org 123 and summarize nodes that are not ready.`
- `Show databases in project 456 and list their DBs and users.`
- `Import services from Git repository repo-abc on branch main.`

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
