# Wodby MCP

Wodby exposes a Model Context Protocol (MCP) server for AI assistants and coding agents that need Wodby context.

Use MCP when you want an AI client to inspect Wodby resources, summarize deployment state, or diagnose failed
operations without manually copying IDs, task logs, and deployment details between tools.

!!! note "Early access"

    The Wodby MCP server currently exposes discovery, diagnostic, and selected operational tools. It is not yet a full
    replacement for the Dashboard, REST API, SDKs, or CLI.

## Endpoint

Use the hosted Wodby MCP endpoint:

```text
https://mcp.wodby.com/mcp
```

The endpoint uses Streamable HTTP. Clients must send MCP JSON-RPC requests over `POST`.

## Authentication

During early access, authenticate MCP requests with a Wodby [API key](api-keys.md) sent as the `X-API-KEY` header.

Create an API key from [User settings > API keys](../user/api-keys.md). Each key belongs to one organization and runs
with the permissions of the user who created it.

Set the key in your shell:

```bash
export WODBY_API_KEY=...
```

## Client configuration

For MCP clients that run local server commands, use `mcp-remote` and pass the Wodby API key as a header:

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

Restart your MCP client after changing its configuration.

Some hosted AI clients do not support custom request headers. Those clients need a future OAuth-based Wodby MCP
connection instead of API-key headers.

## Available tools

Read-only discovery and diagnostic tools:

| Tool | Use |
| --- | --- |
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

Destructive or higher-impact tools require a `confirm: true` argument:

| Tool | Use |
| --- | --- |
| `create_import` | Import data into an app service or database DB. |
| `cancel_task` | Cancel a running task. |
| `upgrade_app_instance_stack` | Upgrade selected app-instance stack sections. |

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

If the MCP server returns `401 Unauthorized`, check that `WODBY_API_KEY` is set in the environment available to your MCP
client process.

If an AI client can list tools but tool calls return access errors, verify that the API key belongs to the organization
you are querying and that the user who created it can view the requested project, app, task, or deployment.

If your client does not send custom headers, it cannot use the early-access API-key MCP connection directly.

## Related pages

- [API keys](api-keys.md)
- [Wodby API](api.md)
- [Wodby CLI](cli.md)
- [Tasks](../tasks.md)
- [Deploys](../apps/deploys.md)
