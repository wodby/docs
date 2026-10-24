# MCP

Connect an AI client to Wodby 1 to inspect resources, deploy applications, manage backups, and troubleshoot tasks. You can also ask an agent to check and apply supported server infrastructure and application stack updates.

!!! note "Availability"
    MCP support for Wodby 1 is upcoming. [Contact support](../support.md) to confirm availability before connecting.

## Connect your client

1. Open `Organization > Agents > Connect an agent`. Choose your client and copy the displayed configuration into the indicated file or terminal.
2. Start authorization from the client. Sign in to Wodby, complete MFA if required, and select the organization to connect.
3. Check the client ID, return address, and permissions. All supported scopes are selected by default. Deselect any you do not want to grant; **Read** is required.
4. Return to your client and send the verification prompt from the Connect page. Verify the organization and its applications before requesting changes.

Terminal setup requires your client's CLI to be installed. If `codex` is not found, follow the [Codex CLI installation instructions](https://learn.chatgpt.com/docs/codex/cli).

For Claude Code, run both commands from the same directory:

```sh
claude mcp add --transport http wodby1 'https://api.wodby.com/api/v3/mcp'
claude mcp login wodby1
```

The first command saves the server configuration. The second starts browser authorization. If the server is already added, run only the login command. Alternatively, enter `/mcp` inside Claude Code, select **wodby1**, and choose **Authenticate**. See [Claude Code authentication](https://code.claude.com/docs/en/mcp#authenticate-from-the-command-line).

For clients with a custom server form, use these settings:

| Setting | Value |
| --- | --- |
| Name | `wodby1` |
| Transport | Streamable HTTP |
| URL | `https://api.wodby.com/api/v3/mcp` |
| Authentication | OAuth |

The client refreshes its access automatically. A connection lasts up to 90 days before another authorization is required. Refreshing keeps the same connection and task history. A new authorization creates a separate connection; revoke connections you no longer use.

### Permissions

OAuth access is restricted to one organization and the authorizing user's existing [permissions](../access-control.md). The approved permissions further limit what the client can do:

| Scope | Permission | Allows |
| --- | --- | --- |
| `mcp:read` | Read | Discover resources and read authorized task logs and diagnostics |
| `mcp:operate` | Operate | Run deployments, backups, cache clears, and other operational tasks |
| `mcp:configure` | Configure | Change application, server, integration, and organization settings |
| `mcp:provision` | Provision | Create resources |
| `mcp:destructive` | Destructive operations | Delete resources, restore or import data, and perform infrastructure or stack upgrades |
| `mcp:sensitive` | Use secrets | Send secrets in supported requests or create temporary connection and upload credentials |

All supported scopes are available during authorization, even when the client initially requests only Read. Your choices take effect when you select **Authorize**. To allow only viewing resources and logs, deselect every scope except Read.

Some tools require more than one permission. To add permissions to an existing connection, authorize again from the client. Refreshing does not add permissions. Destructive operations still require confirmation of the operation and target.

OAuth tokens work only with the Wodby 1 MCP endpoint. They cannot authenticate ordinary API requests or authorize a different organization. Browser sign-in does not authorize third-party Git or cloud-provider integrations.

### API keys for automation

Select **Use an API key** on the Connect page for unattended clients or clients without OAuth support. Enter an agent name, choose an expiration, and select **Create API key**. Save the key before selecting **I have saved the key**; it is shown only once.

Use the same Streamable HTTP URL with an `X-API-Key` header containing the saved key. The Connect page provides client-specific configuration using `WODBY_API_KEY`. Keep the key out of conversations, source control, and logs. Use a separate connection for each integration.

Existing [organization-scoped API keys](../user/api-keys.md) also work. Ordinary keys are not automatically listed as agent connections. API keys use the owner's existing permissions and do not have OAuth permission scopes.

Expand **Tool selection** in API-key setup to choose tool groups or offer read-only tools. The displayed configuration updates with your choices. These URL preferences select tools; they do not restrict the key's permissions.

## Review access and activity

The Agents pages are also available from the organization settings tabs.

Open `Organization > Agents > Connections` to see the authorizing
user, authentication method, approved permissions, credential status, expiration, and last successful MCP tool call under **Last used**. The list includes expired and revoked connections without pagination.

**Authorized** means the credential is available; it does not mean an agent is
running. Initialization alone does not count as a successful tool call. Check
that the agent can identify your organization and list its applications.

You can revoke your own connections. Owners can manage all
organization connections. Administrators can view all connections and manage
member-owned connections, but cannot manage another administrator's or owner's
connection. Support has read-only visibility. Resource permissions still apply
to every operation.

Select **Revoke access** to prevent new authenticated requests with that credential.
Revoked connections remain in the list. Tasks already started may continue;
revoking access does not undo their changes. Remove the saved credential from
the client as well when retiring an integration.

Use **Activity**, or a connection's **Activity** link, to inspect visible tasks
initiated through MCP. Task history shows the initiating tool and a request ID
for troubleshooting. It records task-backed operations, not every read or the
agent's conversation. Older tasks may have no MCP attribution. Viewing a
connection does not grant access to additional task logs or resources.

If an API-key creation response is lost, check Connections before creating
another one. If a key was created but never received, revoke that connection
and create a replacement.

## Choose tools for your workflow

The default connection offers all available tools. To load a smaller catalog,
add `?groups=deployment,data` to the endpoint URL. Choose one or more of
`deployment`, `configuration`, `data`, `infrastructure`, `stacks`, `integrations`,
`organization`, and `billing`. Discovery and task-reading tools remain available.

Add `read_only=1` to offer only tools marked as reads, for example
`https://api.wodby.com/api/v3/mcp?groups=infrastructure&read_only=1`.
These settings limit this connection's tools. They do not change its permissions;
OAuth scopes and the user's resource permissions still apply.

## Workflow guidance

The server includes skills that guide the agent through common Wodby 1 workflows. The agent can call `get_wodby1_guidance` without a name to list the skills, then load the relevant skill by name. You do not need to install a separate skills package.

| Skill | Use it for |
| --- | --- |
| `wodby1-get-started` | Finding organizations, applications, instances, servers, and stacks |
| `wodby1-server-infrastructure-upgrade` | Checking, applying, and verifying offered infrastructure updates |
| `wodby1-stack-upgrade` | Updating organization stacks, upgrading instances, and handling required CI rebuilds |
| `wodby1-deploy` | Creating applications and instances, direct Git deployments, and retained CI builds |
| `wodby1-data` | Backups, restore, cloning, archive imports, and server migration |
| `wodby1-configure` | Service settings, environment variables, domains, cron, and caches |
| `wodby1-troubleshoot` | Following tasks and logs, investigating failures, and checking uncertain outcomes |

Skills help the agent choose and sequence tools. They do not change your permissions or replace your approval of an operation.

### Search the documentation

Ask the agent to use `search_wodby1_docs` for Wodby 1 settings, limits, or
workflow instructions, then `read_wodby1_docs` for the matching page. Long pages
include a continuation offset. The returned URL lets you check the source.
Documentation describes the product; use resource tools to inspect your
organization's current state. If a cached result is marked stale, account for
that when reviewing the answer.

### Install skills locally, if supported

Local installation is optional. The [public skill index](https://api.wodby.com/api/v3/mcp/skills)
links to individual workflows and a downloadable archive. Each release has a
versioned index and SHA-256 hashes. Retain those URLs and hashes when pinning a
version for automation; review changes before upgrading.

The archive contains the same workflow text as MCP guidance, portable skill
directories, plugin metadata, and HTTP MCP configuration. Use your client's
supported installation mechanism. If it cannot load the archive, use
`get_wodby1_guidance` instead. The configuration contains a `WODBY_API_KEY`
environment placeholder; configure the key through your client's secret
settings if that placeholder is unsupported. Installing files does not connect
an account or grant permission. Always discover the connected server's current
tools before following an installed workflow.

## Common requests

Name the organization, application, instance, or server you want to work on. Distinguish checking a proposed change from applying it. For example:

```text
List the applications in organization example and show their instance stack versions.
```

```text
Check the available infrastructure update for server web-1. Show the affected
instances, blockers, and interruption warnings before applying any changes.
```

```text
Update the organization stack, then upgrade only the dev instance of application
example. Follow the tasks and tell me whether a CI rebuild is still required.
```

### Prepare creation before applying it

Use `prepare_app_creation`, `prepare_instance_creation`, or
`prepare_server_creation` to review a new resource before creating it. Start
with the organization UUID and the choices you already know. For example:

```text
Prepare a dev instance of my-app in organization example. Show the server,
stack revision, unresolved choices, and blockers. Do not create it yet.
```

The agent should resolve the returned questions and blockers, review exact
stack/service revision choices and server compatibility, then show the proposed
creation call. Required services need a supported revision from the selected
stack. An explicitly selected service list can omit optional services.

`ready: true` means the supplied choices passed preparation checks. It does not
reserve capacity, guarantee provider availability or prices, or approve
creation. The creation operation checks permissions, limits, and current state
again. Approve the target, configuration, and any costs before applying it.
`create_app_instance` creates an instance using its application's stack without
requiring a data copy; use cloning when a copy is intended.

### Deploy and configure an instance

For a deployment, name the application, instance, and requested code source.
For example:

```text
In organization example, deploy the main branch to the dev instance of my-app.
Follow the deployment task and report the deployed commit.
```

The agent can use a connected repository for a [direct Git deployment](../cicd/git.md),
redeploy the current instance configuration, or deploy an eligible
[previous CI build](../apps/builds.md#deploy-a-previous-build). New CI builds run
through your [configured CI pipeline](../cicd/third-party.md).

For configuration changes, specify the service, setting, and desired value.
The agent should read the existing configuration, preserve unrelated settings,
and explain whether applying the change will restart services or require a CI
rebuild. For example:

```text
In organization example, show the PHP memory limit for the dev instance of
my-app. Propose changing it to 256M and explain how the change will be applied.
```

When changing a secret, provide an explicit replacement and ask the agent to
omit it from its report. Masked values are placeholders; omit them from updates to
preserve the stored secrets. Domain changes do not update external DNS
records automatically; see [domains](../apps/domains.md).

### Backups, restore, and migration

Ask the agent to create a backup of the selected database, files, or both and
follow the task to completion. Before restoring, review the backup, instance,
and components to overwrite. A restore replaces those components on the
original instance; it does not restore code, a CI build, or a stack revision.
See [backups](../apps/backups.md) for recovery and retention behavior.

To create another instance using existing data, ask the agent to clone the
selected source database/files into a new instance in the same organization.
Identify the destination server and new instance name explicitly.

For a [server migration](../apps/server-migration.md), the agent checks
eligibility, selects a successful backup, and creates a separate billable copy.
The source remains available. Verify the copy before switching traffic;
DNS, custom-domain certificates, and source deletion require separate steps.

### Server infrastructure updates

The agent checks the next update offered for the selected server and runs its preflight checks. Review the proposed versions, affected instances, blockers, and interruption warnings before approving the update. A preflight check does not apply the update.

Checks expire after 15 minutes and belong to the user who ran them. Run them again if they expire or the server configuration changes. After approval, the agent follows the update task and checks the recorded server version and maintenance state. Check that your applications remain accessible and behave as expected after completion.

If an update's outcome is uncertain, check its task and installed state before retrying. An outcome check does not repeat the update. See [infrastructure maintenance](../infrastructure/maintenance.md) for interruption and recovery guidance.

### Stack upgrades

Updating a stack in your organization and upgrading an application instance are separate operations. An organization stack update alone does not change running applications. Specify which instances the agent may upgrade, and review the stack's changelog and [upgrade guidance](../stacks/maintenance.md) first.

For instances built through [third-party CI](../cicd/third-party.md), a stack upgrade may remain pending until a new build uses the prepared stack revision and is deployed. The agent should report that pending rebuild rather than claim the upgrade is complete. MCP does not run your external CI pipeline.

Deploying a [previous build](../apps/builds.md#deploy-a-previous-build) selects its saved images and stack revision. It is not a substitute for rebuilding against an upgraded stack, and it does not restore the database or persistent files.

### Import a local archive

Ask the agent to load `wodby1-data` and select the archive and organization.
`prepare_archive_upload` returns a private upload form valid for one hour, with
a maximum archive size of 2 GiB. The agent's client must have permission and
file-transfer support to upload your chosen file. After a successful upload,
the agent can use the returned file URL for a supported import. See the
[Drupal](../stacks/drupal/index.md#import) or [WordPress](../stacks/wordpress/index.md#import) import requirements.

Treat the upload form as a credential and keep it out of shared conversations
and logs. Importing into an existing instance can overwrite data; create a
fresh backup and review the exact target and components first.

### Download an invoice

Ask the agent to list the organization's invoices and retrieve the selected
invoice with `get_invoice_document`. Your key's owner must have permission to
view organization billing. The client must support saving embedded MCP
resources. PDF downloads are limited to 2 MiB.

### Follow tasks to completion

Creating, deploying, upgrading, backing up, or restoring a resource can return a task. Ask the agent to follow that task and inspect its logs before reporting completion. An accepted request is not a completed operation.

Write tools accept an optional `request_key` of 16–128 ASCII letters, digits,
underscores, or hyphens. Ask the agent to use a unique key for each intended
write and preserve it if the same request is submitted again. Duplicate keys
for the same user and organization are refused for 24 hours. This protection requires the
key; it does not repeat or recover the original response. Do not switch keys to
repeat an operation whose outcome is uncertain.

If a request times out or the connection is lost, the change may already have happened. Inspect the task and resource state before retrying. Review the exact target and data impact before confirming deletion, restoration, import, or migration.

!!! warning "Existing data can be overwritten"
    Restoring a backup or importing into an existing instance can overwrite its data. Review the [backup and restore guidance](../apps/backups.md) before approving an overwrite.

### Read diagnostic logs

For task logs, `get_task_log_page` returns the latest messages by default.
Follow `next_before_sequence_id` to find earlier errors. To read new messages,
use `after_sequence_id` with the previous last sequence; zero starts at the
beginning. These cursors are exclusive and cannot be combined.

A page contains at most 100 entries and 64 KiB of encoded entries.
`collection_complete` describes task-log collection, not application health.
Disabled task logging is reported as unavailable. Oversized details are omitted
whole with `details_omitted`; inspect the dashboard task log for that missing
evidence. Other oversized messages are marked truncated. Missing text is not
an empty result or proof of success.

For service logs, `get_instance_service_log_snapshot` freezes the current
rolling cache. Continue with its `snapshot_id`, the same instance/service, and
sequence cursors. Snapshots retain at most 200 entries and 64 KiB of encoded
entries for five minutes. They require the original credential and current
resource access. Source messages larger than 8 KiB are omitted whole.

The service cache can aggregate output from multiple pods, lag, lose batches,
or retain older output after a restart. Check cache presence, update time,
staleness, truncation, and reported gaps. A cache-read failure is an error;
empty or missing cached output does not prove application health.

### Watch logs during a reproduction

For example:

```text
Watch the php service logs for my-app's dev instance for up to 60 seconds while
I reproduce this error. Do not send requests to the app or change it.
```

The agent starts `start_instance_service_log_watch` before the reproduction,
polls `read_instance_service_log_watch` about every five seconds using its
sequence cursor, and calls `stop_instance_service_log_watch` when enough
evidence is collected. A watch polls the existing cache; it is not a complete
runtime stream.

Watches last 60 seconds by default, with a 10–120 second limit, and stop after
30 seconds without a read. Stopped or expired watches cannot resume. Evidence
expires five minutes after creation. Up to three watches and ten snapshots per
user can be admitted within five minutes; shared capacity limits can also
refuse a new collection. Wait for the returned retry interval.

Watch buffers retain at most 200 entries and 64 KiB. Report dropped entries,
cursor gaps, stale cache, and observed target changes. Cached pod observations
cannot guarantee generation coverage. Retained reads require the original
credential and current resource access. Starting a watch does not authorize
commands, test traffic, restarts, or deployments.

## Current limits

MCP does not yet cover every dashboard action:

- Manage account SSH keys and API keys, change passwords, configure MFA, and change organization security requirements in the dashboard.
- Complete third-party OAuth consent and credential verification in the dashboard. Do not send passwords, MFA codes, or recovery codes to the agent.

For bring-your-own-server setup, the agent can prepare an installer command. That does not install or access the server. Treat the command as a credential and run it only on the intended server; see [connecting a server](../infrastructure/connecting-server.md).

Connecting MCP does not grant access to your source repository, host, database, DNS provider, or external CI service. Provide any required access separately.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Authentication fails | For OAuth, start authorization again from the client. For an API key, confirm it was saved correctly and has not expired or been revoked. |
| The endpoint returns `404 Not Found` | Check the Wodby 1 URL above and confirm MCP availability with support. |
| An organization or resource is missing | Confirm the connection's organization and the authorizing user's resource permissions. |
| The client asks for OAuth login | Sign in to Wodby and review the organization and permissions. For API-key automation, choose the client's custom-header configuration. |
| A tool reports insufficient permissions | Authorize the additional permissions from the client. Your Wodby resource permissions still apply. |
| Refresh fails or authorization expires | Start authorization again. If a refresh result was lost, let the client retry promptly; do not repeatedly reuse an old refresh token. |
| Client registration or metadata fails | Check that the client supports public OAuth with S256 PKCE and has valid HTTPS or loopback return addresses. Contact the client provider if its public metadata cannot be loaded. |
| Opening the endpoint in a browser returns `405 Method Not Allowed` | Connect through a Streamable HTTP MCP client. Opening the URL in a browser is not a connection test. |
| The server reports a request limit | Wait at least the returned retry interval before submitting again. Defaults are 120 requests and 30 writes per minute per user and organization. |
| A write reports a duplicate `request_key` | Inspect its target and recent tasks. The original operation may already have run. |
| An operation fails or stops responding | Inspect its task, logs, and current resource state before retrying. |

For connection issues that persist, [contact support](../support.md) with the client name, error message, and relevant task ID. Omit API keys, installer commands, upload forms, and replacement secrets.
