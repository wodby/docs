# Use Wodby with an agent

Connect an AI client to Wodby to inspect applications, plan deployments, and carry out operations you authorize.
This guide applies to Wodby 2. It does not connect an agent to Wodby 1.

## Before you connect

- Sign in to Wodby and choose the organization and project you intend to use. Your agent cannot exceed your own
  [resource permissions](../access-control.md).
- Use a client that supports remote HTTP MCP and OAuth, or the documented API-key fallback.
- If the job involves an existing codebase, give your client access to that repository separately. Wodby MCP does
  not read local files or grant access to your current host, database, or DNS provider.
- Review what your AI provider stores and who can access the conversation. Logs may contain private application data.

You do not need to provision a cluster to connect and inspect resources. Creating resources later can incur charges.

## 1. Connect your client

Follow [Connect your client](clients.md). The endpoint is:

```text
https://mcp.wodby.com/mcp
```

Approve the intended organization and start with `mcp:read`. A successful connection or a visible tool list does not
prove that you have access to a particular application.

## 2. Verify the account and target

Ask:

```text
Use Wodby to identify my authenticated user and list the organizations and projects I can access.
Do not create or change anything. Ask which organization and project to use if the target is ambiguous.
```

Check the returned identity and organization against your intended account. If they are wrong, stop and reconnect
with the correct grant. Do not continue with a similarly named app in another organization.

## 3. Load the relevant workflow

```text
Load Wodby's wodby2-get-started guidance. Check what is needed for this application and list unresolved choices.
Do not provision resources or deploy anything.
```

The agent can use `get_wodby_guidance` to load [workflow skills](skills.md); installing a local plugin is optional.
Skills explain how to work. They do not authenticate the client or authorize changes.

## 4. Complete a read-only check

For an existing Wodby app, replace these example names:

```text
Show the status of app example in organization acme, including its staging environment and latest deployment.
Report the task IDs and anything you could not inspect. Do not change the application.
```

Expected result: the resolved target, deployment/runtime evidence, and any missing permissions or data. An empty log
or a successful log-access task is not proof that the application is healthy.

## 5. Authorize a specific next step

Review the target, operation, cost, data impact, and verification plan before granting additional scopes. Client-side
approval and Wodby permissions are separate. See [Permissions and audit history](permissions.md).

Choose a walkthrough:

- [Assess and plan a migration](workflows/migrate.md) for an application running elsewhere.
- [Deploy and verify staging](workflows/staging.md) for an approved deployment.
- [Diagnose failures and watch logs](workflows/troubleshoot.md) for an existing Wodby application.

For an integration failure, use [Agent connection troubleshooting](troubleshooting.md). For tool schemas, response
handling, and limits, use the [MCP reference](../dev/mcp.md).
