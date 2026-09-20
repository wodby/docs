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

The [diagnostic log reference](../../dev/mcp.md#reading-diagnostic-logs) documents cursors, bounds, and access tasks.
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

See [Watching a live reproduction](../../dev/mcp.md#watching-a-live-reproduction) for exact limits and stop conditions.

## 4. Review the diagnosis and any fix separately

Ask for evidence, likely cause, alternative explanations, missing checks, and the proposed fix with its risks.
Require a new approval before an operational change. After an approved fix, verify the new task and runtime evidence;
do not reuse the previous diagnosis as proof of recovery.

If access is missing, request the appropriate permission or provide a human handoff. If a write has an uncertain
outcome, inspect related tasks and resources before retrying. Finish with task IDs and a clear statement of what
changed, what was verified, and what remains unknown.
