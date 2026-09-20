# Connect your client

Use the hosted Wodby endpoint with a client that supports remote HTTP MCP. Prefer OAuth and begin with read access.
These examples follow the clients' documented configuration formats; client features and organization policies can
vary. A listed configuration is not a certification of every client version. Complete the read-only verification
at the end before authorizing changes.

## Generic clients

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

## API-key fallback

For clients or scripts that cannot complete OAuth, use a dedicated [API key](../dev/api-keys.md) and
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

## Claude Desktop

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

## Claude Code

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

## Codex

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
[scopes](../dev/mcp.md#authentication).

Codex stores MCP servers in `~/.codex/config.toml`, or in `.codex/config.toml` for a trusted project. The equivalent
manual configuration is:

```toml
[mcp_servers.wodby]
url = "https://mcp.wodby.com/mcp"
```

In the Codex terminal UI, use `/mcp` to check connected MCP servers.

See the [official Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp) for client configuration options.

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

## OpenCode

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

## Hermes

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

## Models, hosts, and restricted plugin clients

The host connects to MCP and enforces its own tool-approval policy. Choosing a model through OpenRouter does not
configure a Wodby connection; configure the MCP-capable host that uses that model.

For a client that only accepts marketplace plugins, such as a Grok Bot setup with that restriction, confirm an
appropriate Wodby plugin is actually available and permitted by your administrator. The downloadable Wodby skill
archive is not proof of a marketplace listing. If the host cannot accept the endpoint or a suitable plugin, use a
client with documented remote MCP support rather than guessing setup commands.

## Verify the connection

Ask the agent to identify the authenticated user and list organizations and projects, without making changes.
Confirm the intended organization before inspecting an application. Then load `wodby2-get-started` through
`get_wodby_guidance`. See the [quickstart](index.md) for expected results.

A configured server or successful `tools/list` response alone does not prove the credential can read your target.
Use [connection troubleshooting](troubleshooting.md) if verification fails. For client logout and Wodby-side
revocation, see [Permissions and audit history](permissions.md#expiration-and-revocation).
