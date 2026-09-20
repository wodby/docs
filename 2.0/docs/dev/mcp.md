# MCP

Connect your AI client to Wodby to inspect applications, plan migrations, deploy, and troubleshoot.
This guide applies to Wodby 2.

## Before you connect

- Sign in to Wodby and choose the organization you want the client to access.
- Use an MCP-capable client. Prefer OAuth and start with `mcp:read`.
- Give your client repository access separately when needed. MCP does not grant access to your existing host,
  database, or DNS provider.

Your client acts within your [Wodby permissions](../access-control.md). Connecting does not authorize changes.
Review costs and data impact before approving operations. Logs may contain private application data; never paste
credentials into a conversation. Ordinary API keys do not have OAuth scope restrictions.

## Connect your client

<span id="endpoint"></span>
<span id="client-configuration"></span>

Use this remote HTTP endpoint:

```text
https://mcp.wodby.com/mcp
```

Open the instructions for your client. Merge configuration with existing entries rather than replacing them.
Client versions and organization policies can affect available features.

<span id="codex"></span>

??? note "Codex"

    Codex can add Wodby from the CLI:

    ```bash
    codex mcp add wodby --url https://mcp.wodby.com/mcp
    ```

    If Codex does not open the authorization flow during add, run:

    ```bash
    codex mcp login wodby
    ```

    For an authorized task that needs operational permissions, explicitly request them:

    ```bash
    codex mcp login wodby --scopes mcp:read,mcp:operate
    ```

    Review the new browser consent before approving. Other operations may require different
    [scopes](mcp/reference.md#authentication).

    Codex stores MCP servers in `~/.codex/config.toml`, or in `.codex/config.toml` for a trusted project. The equivalent
    manual configuration is:

    ```toml
    [mcp_servers.wodby]
    url = "https://mcp.wodby.com/mcp"
    ```

    In the Codex terminal UI, use `/mcp` to check connected MCP servers.

    See the [official Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp) for client configuration options.

    For manual-key configuration, see **API-key fallback** below.

<span id="claude-code"></span>

??? note "Claude Code"

    Claude Code can connect to remote HTTP MCP servers directly:

    ```bash
    claude mcp add --transport http wodby https://mcp.wodby.com/mcp
    ```

    Then run the OAuth login flow (in versions that support CLI login):

    ```bash
    claude mcp login wodby
    ```

    Alternatively, start Claude Code and use `/mcp` to authorize Wodby. Check the server with `claude mcp get wodby`.
    See the [Claude Code MCP reference](https://code.claude.com/docs/en/mcp).

<span id="claude-desktop"></span>

??? note "Claude Desktop"

    Install Node.js and npm, and make sure Claude Desktop can find `npx`.

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

<span id="opencode"></span>

??? note "OpenCode"

    Add this entry to your `opencode.json`, merging it with any existing configuration:

    ```json
    {
      "$schema": "https://opencode.ai/config.json",
      "mcp": {
        "wodby": {
          "type": "remote",
          "url": "https://mcp.wodby.com/mcp",
          "enabled": true
        }
      }
    }
    ```

    Then authorize and inspect the connection:

    ```bash
    opencode mcp auth wodby
    opencode mcp list
    ```

    Review the organization and scopes in browser consent. See [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/).

<span id="hermes"></span>

??? note "Hermes"

    Merge this into `~/.hermes/config.yaml`:

    ```yaml
    mcp_servers:
      wodby:
        url: "https://mcp.wodby.com/mcp"
        auth: oauth
    ```

    Run authorization from a fresh terminal, then restart the session or use `/reload-mcp`:

    ```bash
    hermes mcp login wodby
    ```

    A remote gateway needs a supported callback or interactive authorization handoff. Do not assume that a device-code
    flow is available on Wodby. See [Hermes MCP configuration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/).

<span id="generic-clients"></span>

??? note "Generic clients"

    Install Node.js and npm first, and make sure your client can find `npx`.

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

<span id="api-key-fallback"></span>

??? note "API-key fallback"

    For clients or scripts that cannot complete OAuth, use a dedicated [API key](api-keys.md) and
    `X-API-KEY`. Ordinary API keys do not gain the restrictions of an OAuth scope grant:

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

    Provide `WODBY_API_KEY` through the environment of the client process or its supported secret store. Desktop apps
    started from a launcher may not inherit variables exported in a terminal. Do not replace the placeholder with a
    literal key in a shared configuration file.

    **Codex:**

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

<span id="models-hosts-and-restricted-plugin-clients"></span>

??? note "Other hosts and models"

    The host connects to MCP and enforces its own tool-approval policy. Choosing a model through OpenRouter does not
    configure a Wodby connection; configure the MCP-capable host that uses that model.

    For a client that only accepts marketplace plugins, such as a Grok Bot setup with that restriction, confirm an
    appropriate Wodby plugin is actually available and permitted by your administrator. The downloadable Wodby skill
    archive is not proof of a marketplace listing. If the host cannot accept the endpoint or a suitable plugin, use a
    client with documented remote MCP support rather than guessing setup commands.

## Verify the connection

<span id="using-wodby-in-your-mcp-client"></span>

Approve the intended organization in browser consent, then ask:

```text
Use Wodby to identify my user and list the organizations and projects I can access.
Do not change anything. Ask which project to use if the target is ambiguous.
```

Confirm the returned identity and target. A configured server or visible tool list does not prove access to an app.
If the account is wrong or access fails, stop and use [connection troubleshooting](../agents/troubleshooting.md).

For an existing application, replace these example names:

```text
Show the status of app example in organization acme, including staging and its latest deployment.
Report missing evidence. Do not change the application.
```

## Choose a task

<span id="agent-workflows"></span>

Ask the agent to load `wodby2-get-started` with `get_wodby_guidance`, or choose a walkthrough:

- [Plan a migration](../agents/workflows/migrate.md) for an application hosted elsewhere.
- [Deploy staging](../agents/workflows/staging.md) after reviewing the target and costs.
- [Diagnose a failure](../agents/workflows/troubleshoot.md) using task logs and runtime evidence.

[Skills](../agents/skills.md) provide the workflow; tools perform individual steps. Installing skills locally is optional.
Read [Permissions and audit history](../agents/permissions.md) before granting more access.
A plan does not approve deployment, and staging approval does not approve production cutover.

## Technical reference

<span id="custom-clients"></span>
<span id="response-handling"></span>
<span id="authentication"></span>
<span id="discovery-examples"></span>
<span id="diagnostics-examples"></span>
<span id="reading-diagnostic-logs"></span>
<span id="watching-a-live-reproduction"></span>
<span id="operation-examples"></span>
<span id="cluster-database-and-catalog-examples"></span>
<span id="service-provider-and-stack-manifest-examples"></span>
<span id="sensitive-and-destructive-examples"></span>
<span id="available-tools"></span>
<span id="read-tools"></span>
<span id="operation-tools"></span>
<span id="configuration-tools"></span>
<span id="provisioning-tools"></span>
<span id="sensitive-tools"></span>
<span id="destructive-tools"></span>
<span id="choosing-mcp-api-sdks-or-cli"></span>
<span id="troubleshooting"></span>
<span id="related-pages"></span>

For custom clients and exact behavior, see the [protocol, authentication, task, and log reference](mcp/reference.md)
and [tool catalog](mcp/tools.md). Use the connected server's schemas for current inputs and capabilities.
