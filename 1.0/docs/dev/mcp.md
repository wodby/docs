# MCP

Connect an AI client to Wodby 1 to inspect resources, deploy applications, manage backups, and troubleshoot tasks. You can also ask an agent to check and apply supported server infrastructure and application stack updates.

!!! note "Availability"
    MCP support for Wodby 1 is upcoming. [Contact support](../support.md) to confirm availability before connecting.

## Connect your client

1. Create an [organization-scoped API key](../user/api-keys.md) under `Account > API Keys`. Use a separate key for each agent integration.
2. In your MCP client's server settings, add a remote server with these values:

    | Setting | Value |
    | --- | --- |
    | Name | `wodby1` |
    | Transport | Streamable HTTP |
    | URL | `https://api.wodby.com/api/v3/mcp` |
    | Authentication header | `X-API-Key` |
    | Header value | Your Wodby 1 API key |

3. Save the key in your client's secret configuration, then connect and load the server's tools. Keep the key out of conversations, source control, and logs.
4. Ask the agent to list the organization and its applications. Verify the organization before requesting changes.

Your client must support remote HTTP MCP servers with custom authentication headers. Clients that require OAuth browser authorization cannot use this endpoint. Wodby 1 and Wodby 2 use different MCP endpoints and connection settings.

The agent acts with the key owner's [permissions](../access-control.md), restricted to the key's organization. Connecting does not grant additional permissions or authorize changes. API keys do not provide separate MCP read-only scopes; use an account with permissions appropriate to the work you want the agent to perform.

## Choose tools for your workflow

The default connection offers all available tools. To load a smaller catalog,
add `?groups=deployment,data` to the endpoint URL. Choose one or more of
`deployment`, `configuration`, `data`, `infrastructure`, `stacks`, `integrations`,
`organization`, and `billing`. Discovery and task-reading tools remain available.

Add `read_only=1` to offer only tools marked as reads, for example
`https://api.wodby.com/api/v3/mcp?groups=infrastructure&read_only=1`.
These settings limit this connection's tools. They do not change the API key's
permissions; use appropriate account permissions for access restrictions.

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

## Current limits

MCP does not yet cover every dashboard action:

- Manage account SSH keys and API keys, change passwords, configure MFA, and change organization security requirements in the dashboard.
- Complete third-party OAuth consent and credential verification in the dashboard. Do not send passwords, MFA codes, or recovery codes to the agent.

For bring-your-own-server setup, the agent can prepare an installer command. That does not install or access the server. Treat the command as a credential and run it only on the intended server; see [connecting a server](../infrastructure/connecting-server.md).

Connecting MCP does not grant access to your source repository, host, database, DNS provider, or external CI service. Provide any required access separately.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Authentication fails | Confirm the API key was saved correctly and has not expired or been revoked. |
| The endpoint returns `404 Not Found` | Check the Wodby 1 URL above and confirm MCP availability with support. |
| An organization or resource is missing | Confirm the key's organization and its owner's resource permissions. |
| The client asks for OAuth login | Use a client configuration that supports an API key in a custom header. |
| Opening the endpoint in a browser returns `405 Method Not Allowed` | Connect through a Streamable HTTP MCP client. Opening the URL in a browser is not a connection test. |
| The server reports a request limit | Wait at least the returned retry interval before submitting again. Defaults are 120 requests and 30 writes per minute per user and organization. |
| A write reports a duplicate `request_key` | Inspect its target and recent tasks. The original operation may already have run. |
| An operation fails or stops responding | Inspect its task, logs, and current resource state before retrying. |

For connection issues that persist, [contact support](../support.md) with the client name, error message, and relevant task ID. Omit API keys, installer commands, upload forms, and replacement secrets.
