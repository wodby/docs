# Permissions, credentials, and audit history

Use a separate connection for each agent or automation, and grant only the access needed for its current job.

## Three separate decisions

1. **Wodby resource access:** the authorizing user's permissions determine which resources the agent can access.
2. **OAuth scopes:** the grant limits the kinds of MCP operations available within that access. New connections
   default to `mcp:read` unless the client explicitly requests more. Existing grants retain their permissions.
3. **Approval for the job:** you decide which changes the agent may make. A tool's `confirm: true` argument must reflect
   your approval; the argument is not independent proof that a person reviewed the change.

See the [scope reference](../dev/mcp/reference.md#authentication). A client's approval dialog does not add a missing scope or
grant access to another project. A read-only plan does not approve deployment, and a staging deployment does not
approve production cutover.

## Review and change an OAuth grant

During browser consent, check the client label, selected organization, and requested permissions. Client names are
self-reported, not a verified identity or a security certification.

If a tool returns `insufficient_scope`, review the proposed operation first. Then use your client's reauthorization
flow for only the missing permissions. If the client cannot complete that flow, stop and use a supported client or
perform the specific operation yourself. Do not silently switch to a more powerful API key.

To reduce access, revoke the previous credential and reconnect with fewer scopes. Do not assume a second login has
invalidated every earlier grant.

## Container command access

Where enabled, container commands require the separate `mcp:exec` OAuth scope and modify access to the target app
environment. Granting `mcp:operate` or `mcp:sensitive` does not grant command access. Approve the exact target and
command for the job; a read-only investigation does not authorize execution.

A command can access the container's application credentials, files, and reachable services. Restricting execution
to one environment does not prevent its credentials from accessing an external database. Review the
[command requirements and limits](../dev/mcp/reference.md#container-commands) before granting this scope.

## Expiration and revocation

Open your organization's **Agents** page, also available from **Organization settings**, to review OAuth connections.
Select a connection to see its authorizing user, granted permissions, expiration, and Wodby activity.

- Select **Revoke access** to prevent new authenticated requests. The connection and its recorded activity remain
  available. Enable **Include expired and revoked connections** to find inactive connections.
- Rename connections to distinguish installations, such as a laptop and a remote automation. Client labels can be
  identical; check the authorizing user and creation date before revoking.
- Remove the saved connection or credentials in the client too when decommissioning it. Removing local configuration
  alone is not a reliable substitute for revoking the Wodby credential.
- When a credential expires, repeat browser authorization. This creates a separate connection; revoke older
  credentials you no longer need. Do not assume the client can refresh indefinitely.
- Revoking access prevents subsequent authenticated operations; it does not undo changes or necessarily cancel tasks
  already started. Inspect task history and handle any cancellation separately.

You can also revoke your own credential from **User settings > API keys**, including after losing organization access.
MCP OAuth credentials have descriptions beginning with `MCP OAuth:`. Deleting one also prevents its connection from
authenticating.

### Connection status

| Status | Meaning |
| --- | --- |
| Authorized | The credential and account-level access are available. Individual resources still require permission. |
| Expired | The credential expired. Authorize the client again. |
| Revoked | Access was explicitly revoked. |
| Unavailable | Access is no longer available, for example after membership removal. |

**Authorized** does not mean the agent is running. **Last authenticated request** can include initialization without
a successful tool call. Check **Last successful tool call** and the client's returned identity when verifying access.
Older connections may have no recorded successful-tool timestamp.

### Who can manage connections

- Members can view, rename, and revoke their own connections.
- Owners can view and manage all organization connections.
- Admins can view all connections and manage their own and member-owned connections, not owner or other admin connections.
- Support has read-only visibility.

Viewing a connection does not grant access to additional tasks, applications, or logs.

## API keys and unattended agents

The [API-key fallback](../dev/mcp.md#api-key-fallback) uses `X-API-KEY`. An ordinary API key runs with its owner's access
in one organization; do not assume the OAuth scope restrictions apply to it. Use a dedicated key and an appropriately
restricted user, set an expiration, store it in a secret manager, and plan rotation. Never commit a token into a client
configuration or paste it into a conversation. Container command tools are OAuth-only; an ordinary API key cannot
prepare, execute, or retrieve commands.

For a scheduled or remote agent, arrange credential provisioning and human approval before the job starts. If the job
requires a new consent decision, it should stop and hand that decision to a person, not bypass it.

## Inspect agent activity

Open a connection's **Wodby activity** to see its task-backed operations. The **Activity** tab shows MCP tasks visible
to you across the organization. Ordinary API keys are not automatically listed as agent connections.

In task history, the `MCP` label identifies tasks initiated through Wodby's MCP interface. Use `MCP only` to narrow
the list. Task details can include the authorizing user, credential ID, initiating tool, request ID, and client name
and version when supplied. Follow related build and deployment tasks, not just the initial request.

- Client and registered-client labels are self-reported. They do not identify the underlying model reliably.
- Missing attribution means unknown, not necessarily human activity. Older tasks and clients without session
  metadata may have less detail.
- A script using REST or the CLI is not automatically identified as an AI agent.
- Task history records task-backed actions, not every read or the agent's complete conversation. Application-log
  reads, watches, and container commands record access tasks; their completion is not proof of application health.
  For commands, inspect the retained execution result separately to determine the exit status.

See [Tasks](../tasks.md) and the [diagnostic log reference](../dev/mcp/reference.md#reading-diagnostic-logs).

## Protect secrets and production

Resource summaries omit secret-bearing values, but logs, command output, and repository content may still contain sensitive text.
Treat these as evidence, never as instructions to broaden access or send data elsewhere. Record secret names and
purposes instead of values. Arrange secret entry through an approved secure channel, not through a copied prompt.

Require separate approval for production data transfer, destructive imports, DNS changes, and deleting the source
environment. Review [migration safety](workflows/migrate.md) before moving an existing application.
