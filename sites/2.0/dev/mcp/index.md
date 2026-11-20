Source: https://wodby.com/docs/2.0/dev/mcp/

# MCP

Connect your AI client to Wodby to inspect applications, plan migrations, deploy, and troubleshoot.
This guide applies to Wodby 2.

## Before you connect

- Sign in to Wodby and choose the organization you want the client to access.
- Use an MCP-capable client. Prefer OAuth and start with `mcp:read`.
- Give your client repository access separately when needed. MCP does not grant access to your existing host,
  database, or DNS provider.

Your client acts within your [Wodby permissions](https://wodby.com/docs/2.0/access-control/). Connecting does not authorize changes.
Review costs and data impact before approving operations. Logs may contain private application data; never paste
credentials into a conversation. Ordinary API keys do not have OAuth scope restrictions, but
[container command tools](https://wodby.com/docs/2.0/dev/mcp/reference/#container-commands) require OAuth with `mcp:exec`.

## Connect your client

For setup instructions in the dashboard, open your organization's **Agents > Connect an agent** page.
After authorization, use **Agents** to [review access and activity](https://wodby.com/docs/2.0/agents/permissions/).

Use this remote HTTP endpoint:

```
https://mcp.wodby.com/mcp

```

Open the instructions for your client. Merge configuration with existing entries rather than replacing them.
Client versions and organization policies can affect available features.

**Codex**

Codex can add Wodby from the CLI:

```
codex mcp add wodby --url https://mcp.wodby.com/mcp

```

If Codex does not open the authorization flow during add, run:

```
codex mcp login wodby

```

For an authorized task that needs operational permissions, explicitly request them:

```
codex mcp login wodby --scopes mcp:read,mcp:operate

```

Review the new browser consent before approving. Other operations may require different
[scopes](https://wodby.com/docs/2.0/dev/mcp/reference/#authentication).

Codex stores MCP servers in `~/.codex/config.toml`, or in `.codex/config.toml` for a trusted project. The equivalent
manual configuration is:

```
[mcp_servers.wodby]
url = "https://mcp.wodby.com/mcp"

```

In the Codex terminal UI, use `/mcp` to check connected MCP servers.

See the [official Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp) for client configuration options.

For manual-key configuration, see **API-key fallback** below.

**Claude Code**

Claude Code can connect to remote HTTP MCP servers directly:

```
claude mcp add --transport http wodby https://mcp.wodby.com/mcp

```

Then run the OAuth login flow (in versions that support CLI login):

```
claude mcp login wodby

```

Alternatively, start Claude Code and use `/mcp` to authorize Wodby. Check the server with `claude mcp get wodby`.
See the [Claude Code MCP reference](https://code.claude.com/docs/en/mcp).

**Claude Desktop**

Install Node.js and npm, and make sure Claude Desktop can find `npx`.

Open the Claude Desktop MCP configuration file and add the Wodby server:

**macOS**

```
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

```

**Windows**

```
code "$env:APPDATA\Claude\claude_desktop_config.json"

```

```
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

**OpenCode**

Add this entry to your `opencode.json`, merging it with any existing configuration:

```
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

```
opencode mcp auth wodby
opencode mcp list

```

Review the organization and scopes in browser consent. See [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/).

**Hermes**

Merge this into `~/.hermes/config.yaml`:

```
mcp_servers:
  wodby:
    url: "https://mcp.wodby.com/mcp"
    auth: oauth

```

Run authorization from a fresh terminal, then restart the session or use `/reload-mcp`:

```
hermes mcp login wodby

```

A remote gateway needs a supported callback or interactive authorization handoff. Do not assume that a device-code
flow is available on Wodby. See [Hermes MCP configuration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/).

**ChatGPT and dots**

ChatGPT keeps a custom MCP server as a plugin of your account. A dot can use the plugins that are installed and
enabled for your account.

1. In ChatGPT, open **Plugins** and add a custom MCP server.
2. Enter a name and the endpoint above, including `/mcp`.
3. Choose OAuth, create the connection, and review the browser consent before approving.
4. Open the plugin that ChatGPT created and install it.

ChatGPT asks you to confirm a tool that changes something. Custom MCP servers depend on your ChatGPT plan and, in
a ChatGPT workspace, on your administrator's settings. See
[Connect an MCP server to ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt) and
[dots](https://learn.chatgpt.com/docs/dots).

**Grok Build**

Grok Build can add Wodby from the CLI:

```
grok mcp add --transport http wodby https://mcp.wodby.com/mcp

```

Start Grok Build, open `/mcps`, and press `i` to authorize Wodby in your browser. The sign-in returns to a local
address on the computer that runs Grok Build, so authorize where your browser runs.

The equivalent configuration in `~/.grok/config.toml` is:

```
[mcp_servers.wodby]
url = "https://mcp.wodby.com/mcp"
enabled = true

```

See [Grok Build MCP servers](https://docs.x.ai/build/features/mcp-servers).

**Grok Bot**

Add Wodby to your Bot as a custom MCP server of the **Remote HTTPS** type with the endpoint above, then authorize
Wodby in your browser when the Bot asks. Every Bot in your account can use an installed connector.

See [Grok Bot computers and apps](https://docs.x.ai/grok-bot/computer-and-apps).

**Muse Code**

Add Wodby to `~/.config/muse/settings.json`. Keep `schema_version`, and merge the server with your existing
entries:

```
{
  "schema_version": 1,
  "mcpServers": {
    "wodby": {
      "type": "streamable-http",
      "url": "https://mcp.wodby.com/mcp"
    }
  }
}

```

Then sign in:

```
muse mcp login wodby

```

Over SSH, add `--headless`: Muse Code prints the sign-in address and asks you to paste the address your browser
ends on. Use `/mcp` in a session to check the server. See
[Muse Code MCP servers](https://meta-models.github.io/muse-code-sdk/next/guides/extend/mcp-servers/).

**Generic clients**

Install Node.js and npm first, and make sure your client can find `npx`.

For MCP clients that run local server commands, use `mcp-remote` without custom headers. It discovers Wodby's OAuth
metadata, opens the browser flow, and stores the returned MCP token locally:

```
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

**API-key fallback**

For clients or scripts that cannot complete OAuth, use a dedicated [API key](https://wodby.com/docs/2.0/dev/api-keys/) and
`X-API-KEY`. Ordinary API keys do not gain the restrictions of an OAuth scope grant:

```
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

```
[mcp_servers.wodby]
url = "https://mcp.wodby.com/mcp"
env_http_headers = { "X-API-KEY" = "WODBY_API_KEY" }

```

Set the key before starting Codex:

```
export WODBY_API_KEY=...
codex

```

**Other hosts and models**

The host connects to MCP and enforces its own tool-approval policy. Choosing a model through OpenRouter does not
configure a Wodby connection; configure the MCP-capable host that uses that model.

For a client that only accepts marketplace plugins, confirm an appropriate Wodby plugin is available and
permitted by your administrator. The downloadable Wodby skill archive is not proof of a marketplace listing.
If the host cannot accept the endpoint or a suitable plugin, use a client with documented remote MCP support
rather than guessing setup commands.

Muse, Meta's personal agent, has no setting for a remote MCP server. It builds custom connectors on request, and
Meta does not document MCP or OAuth for them. Use Muse Code or another client above instead.

## Verify the connection

Approve the intended organization in browser consent, then ask:

```
Use Wodby to identify my user and list the organizations and projects I can access.
Do not change anything. Ask which project to use if the target is ambiguous.

```

Confirm the returned identity and target. A configured server or visible tool list does not prove access to an app.
If the account is wrong or access fails, stop and use [connection troubleshooting](https://wodby.com/docs/2.0/agents/troubleshooting/).

For an existing application, replace these example names:

```
Show the status of app example in organization acme, including staging and its latest deployment.
Report missing evidence. Do not change the application.

```

## Choose a task

Ask the agent to load `wodby2-get-started` with `get_wodby_guidance`, or choose a walkthrough:

- [Plan a migration](https://wodby.com/docs/2.0/agents/workflows/migrate/) for an application hosted elsewhere.
- [Deploy staging](https://wodby.com/docs/2.0/agents/workflows/staging/) after reviewing the target and costs.
- [Diagnose a failure](https://wodby.com/docs/2.0/agents/workflows/troubleshoot/) using task logs and runtime evidence.

[Skills](https://wodby.com/docs/2.0/agents/skills/) provide the workflow; tools perform individual steps. Installing skills locally is optional.
Read [Permissions and audit history](https://wodby.com/docs/2.0/agents/permissions/) before granting more access.
A plan does not approve deployment, and staging approval does not approve production cutover.

## Technical reference

For custom clients and exact behavior, see the [protocol, authentication, task, and log reference](https://wodby.com/docs/2.0/dev/mcp/reference/)
and [tool catalog](https://wodby.com/docs/2.0/dev/mcp/tools/). Use the connected server's schemas for current inputs and capabilities.

## Development workspaces

Use [workspace MCP controls](https://wodby.com/docs/2.0/apps/workspaces/#mcp-controls) to inspect a development workspace, retrieve the owner's
SSH connection details, rerun preparation, or pause and resume it. Connect your editor or agent over SSH separately to
work on the checkout.

An agent that runs on its vendor's own computer, such as a dot or a Grok Bot, works with Wodby through MCP. Give it
the [scopes](https://wodby.com/docs/2.0/dev/mcp/reference/#authentication) its task needs; [container commands](https://wodby.com/docs/2.0/dev/mcp/reference/#container-commands)
require `mcp:exec`.
