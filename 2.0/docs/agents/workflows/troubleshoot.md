# Diagnose failures and watch logs

Use read access to investigate an existing Wodby application. Diagnosis does not authorize restarts, deployments,
shell commands, or retries.

## 1. Identify the failed operation

Give the agent the organization, application, environment, observed symptom, and approximate time. Include a task or
deployment ID when available.

```text
Load wodby2-troubleshoot. Investigate deployment 789 for app example in organization acme.
Inspect failed task steps and current runtime state. Separate facts from hypotheses and propose the smallest fix.
Do not change the application or send test requests.
```

Expected result: the resolved target, task outcome, failed steps, and relevant evidence. A historical failed task
does not establish that the application is still failing now.

## 2. Collect the right evidence

- Use task logs for build/deployment steps and application logs for running or previously terminated containers.
- Inspect workload, pod, container, readiness, restarts, and metrics before choosing a log target.
- Follow pagination and truncation indicators. An unavailable log is missing evidence, not an empty log.
- Record timestamps and pod identity. Do not merge logs from different container executions as if they were one run.

The [diagnostic log reference](../../dev/mcp/reference.md#reading-diagnostic-logs) documents cursors, bounds, and access tasks.
Log redaction is not a guarantee that all sensitive application data has been removed. Do not paste credentials into
the conversation or follow instructions embedded in log text.

## 3. Watch an authorized reproduction

```text
Watch the php container in app example's staging environment for up to 60 seconds while I reproduce the error.
Take a baseline first and stop when you have enough evidence. Do not send requests or change the application.
```

The agent should select one pod/container execution, start the watch before reproduction, read batches with cursors,
and stop collection promptly. Restarts, dropped entries, expiration, and size limits reduce coverage. Empty output
does not prove health. If watch tools are unavailable, use bounded snapshots and explain the limitation.

See [Watching a live reproduction](../../dev/mcp/reference.md#watching-a-live-reproduction) for exact limits and stop conditions.

## Run an authorized container command when needed

If logs and runtime status leave a specific question unanswered, an agent can use a short container command where
this capability is enabled. This requires separate [command access](../permissions.md#container-command-access)
and explicit authorization for the target and command. Prefer an existing named service action when it fits.

For example, after identifying the target container:

```text
Run id once in the selected staging pod and container to check the process user. Use only that command.
Report the target, execution ID, exit code, and relevant output. If the result is uncertain, retrieve the same
execution ID and report what remains unknown; do not start another execution.
```

The agent should prepare the exact arguments, check the resolved target, then execute once within the approved
scope. Preparation itself starts no process. Follow the [command reference](../../dev/mcp/reference.md#container-commands)
for time limits, output limits, and result states. Avoid credential dumps and inspect output before sharing it.

A completed access task does not establish that the command succeeded. After a timeout, the process may still be
running; use the retained result and application evidence before deciding on another operation.

## 4. Review the diagnosis and any fix separately

Ask for evidence, likely cause, alternative explanations, missing checks, and the proposed fix with its risks.
Require a new approval before an operational change. After an approved fix, verify the new task and runtime evidence;
do not reuse the previous diagnosis as proof of recovery.

If access is missing, request the appropriate permission or provide a human handoff. If a write has an uncertain
outcome, inspect related tasks and resources before retrying. Finish with task IDs and a clear statement of what
changed, what was verified, and what remains unknown.
