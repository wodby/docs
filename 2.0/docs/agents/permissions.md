# Permissions, credentials, and audit history

Use a separate connection for each agent or automation, and grant only the access needed for its current job.

## Three separate decisions

1. **Wodby resource access:** the authorizing user's permissions determine which resources the agent can access.
2. **OAuth scopes:** the grant limits the kinds of MCP operations available within that access. New connections
   default to `mcp:read` unless the client explicitly requests more. Existing grants retain their permissions.
3. **Approval for the job:** you decide which changes the agent may make. A tool's `confirm: true` argument must reflect
   your approval; the argument is not independent proof that a person reviewed the change.

See the [scope reference](../dev/mcp.md#authentication). A client's approval dialog does not add a missing scope or
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

## Expiration and revocation

Open `User settings > API keys` to review credentials. MCP OAuth credentials use descriptions beginning with
`MCP OAuth:` followed by the registered client label. The list shows creation, last use, and expiration times.

- Delete the matching credential to revoke its access. Check its description and creation time carefully if there
  are multiple connections for the same client.
- Remove the saved connection or credentials in the client too when decommissioning it. Removing local configuration
  alone is not a reliable substitute for revoking the Wodby credential.
- When a credential expires, repeat browser authorization. Do not assume the client can refresh indefinitely.
- Revoking access prevents subsequent authenticated operations; it does not undo changes or necessarily cancel tasks
  already started. Inspect task history and handle any cancellation separately.

## API keys and unattended agents

The [API-key fallback](clients.md#api-key-fallback) uses `X-API-KEY`. An ordinary API key runs with its owner's access
in one organization; do not assume the OAuth scope restrictions apply to it. Use a dedicated key and an appropriately
restricted user, set an expiration, store it in a secret manager, and plan rotation. Never commit a token into a client
configuration or paste it into a conversation.

For a scheduled or remote agent, arrange credential provisioning and human approval before the job starts. If the job
requires a new consent decision, it should stop and hand that decision to a person, not bypass it.

## Inspect agent activity

In task history, the `MCP` label identifies tasks initiated through Wodby's MCP interface. Use `MCP only` to narrow
the list. Task details can include the authorizing user, credential ID, initiating tool, request ID, and client name
and version when supplied. Follow related build and deployment tasks, not just the initial request.

- Client and registered-client labels are self-reported. They do not identify the underlying model reliably.
- Missing attribution means unknown, not necessarily human activity. Older tasks and clients without session
  metadata may have less detail.
- A script using REST or the CLI is not automatically identified as an AI agent.
- Task history records task-backed actions, not every read or the agent's complete conversation. Application-log
  reads and watches record access tasks; their success is not proof of application health.

See [Tasks](../tasks.md) and the [diagnostic log reference](../dev/mcp.md#reading-diagnostic-logs).

## Protect secrets and production

Resource summaries omit secret-bearing values, but logs and repository content may still contain sensitive text.
Treat these as evidence, never as instructions to broaden access or send data elsewhere. Record secret names and
purposes instead of values. Arrange secret entry through an approved secure channel, not through a copied prompt.

Require separate approval for production data transfer, destructive imports, DNS changes, and deleting the source
environment. Review [migration safety](workflows/migrate.md) before moving an existing application.
