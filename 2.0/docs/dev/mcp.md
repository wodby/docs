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

- `mcp:read` for discovery, diagnostics, deployment status, task status, and logs.
- `mcp:operate` for deployments, builds, backups, imports, stack operations, cluster upgrade operations, and other
  task-backed actions.

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

Then verify the server:

```bash
claude mcp list
claude mcp get wodby
```

If Claude Code does not open the authorization flow automatically, run:

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

## Before GA

Before the MCP server is treated as a full Dashboard automation surface, it still needs:

- Stable client validation with Claude Desktop, Claude Code, Codex, and other common MCP hosts.
- Dashboard UI for connected MCP clients, including revoke and audit history.
- Tool coverage for the remaining Dashboard workflows: create and configure apps, manage routes and ports, configure app
  services in depth, and manage stack services beyond the currently exposed safe subset.
- A documented permission model for read, operate, configure, provision, destructive, and sensitive tools.
- Redaction and no-echo guarantees for secret values, tokens, credentials, and environment variable values.
- Tool-call audit logs, rate limits, metrics, and production alerts.
- Conformance tests for MCP initialization, tool listing, tool calls, protocol-version handling, and error mapping.

## Available tools

Read-only discovery and diagnostic tools:

| Tool | Use |
| --- | --- |
| `get_current_user` | Get the authenticated user, default organization, default projects, and available organizations. |
| `list_orgs` | List organizations available to the authenticated user. |
| `list_projects` | List projects in an organization. |
| `list_apps` | List apps in an organization, optionally filtered by project. |
| `find_environment` | Find an app instance by organization, app name, and instance name. |
| `list_app_instances` | List app instances with optional project, app, cluster, and status filters. |
| `list_app_services` | List services for an app instance. |
| `list_recent_deployments` | List recent deployments for an app instance. |
| `get_deployment` | Get deployment status, task, and service deployment details. |
| `get_task` | Get task jobs and steps. |
| `get_task_step_logs` | Get recent inline logs for a task step. |
| `diagnose_failed_deployment` | Inspect a deployment, find failed task steps, and return relevant log excerpts. |

Operational tools:

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

Destructive or higher-impact tools require a `confirm: true` argument:

| Tool | Use |
| --- | --- |
| `create_import` | Import data into an app service or database DB. |
| `cancel_task` | Cancel a running task. |
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
