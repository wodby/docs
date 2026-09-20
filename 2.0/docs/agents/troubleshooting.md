# Agent connection troubleshooting

Start with the [read-only connection check](../dev/mcp.md#verify-the-connection).
Do not test connection problems by creating or deleting resources.

| Symptom | What to check | Safe next step |
| --- | --- | --- |
| Connection appears configured, but no tools are available | Whether the host loaded the configuration, allows this server, and supports remote HTTP MCP | Restart/reload the client and inspect its MCP status. |
| `401 Unauthorized` | Expired/revoked credentials or a key unavailable to the client process | Reauthorize; for API keys check the injected environment, without printing the secret. |
| Browser consent does not open | OAuth support, browser access, and callback handling in the client | Use the client's documented login flow; arrange a human handoff for remote/unattended jobs. |
| `insufficient_scope` | The grant lacks permission for this operation | Review the operation, then request only the needed scopes through new consent. |
| Access denied despite sufficient scopes | Wrong organization or missing user/project access | Resolve the intended target and request resource access. More scopes cannot override resource permissions. |
| Expected tool is missing | Client filtering or a server/client capability difference | Refresh discovery, inspect live schemas, and use a documented fallback or dashboard handoff. |
| MCP session expired or invalid | A stale session or a session reused with different credentials | Initialize again with the current credential; do not reuse another agent's session ID. |
| Request timed out after a change | The operation may already have started | Inspect the target and related tasks before retrying. |
| Watch ended or logs are empty | Target restart, retention/size limits, dropped entries, or no new output | Report incomplete coverage; rediscover the target before another bounded read. |

See [client setup](../dev/mcp.md#connect-your-client), [credential management](permissions.md), and
[MCP error handling](../dev/mcp/reference.md#troubleshooting). Never post tokens, authorization URLs containing codes, or
unredacted application secrets when asking for help.

## Information to include in a support request

Provide the client and version, transport, time of failure, error code, affected organization/resource IDs, and task
or MCP request ID when available. Explain whether the last action was read-only or could have changed resources.
Include a short redacted error excerpt and the checks already performed. Do not include API keys or OAuth tokens.
