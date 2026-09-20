# Deploy and verify staging

Use this walkthrough after selecting an application, stack, and target environment. For an application running
elsewhere, first complete the [migration assessment](migrate.md).

## Requirements

- Confirm the organization, project, stack revision, cluster, repository revision, and intended staging name.
- Arrange required Git/build integrations and secret entry. The agent cannot assume access to these systems.
- Approve any resource costs and data transfer. Start with read access; grant provisioning, configuration, or
  operation scopes only for the actions in the approved plan.
- Isolate databases, queues, persistent storage writes, email, webhooks, workers, and schedules from production.
  If isolation is not possible, stop before starting components that can produce side effects.

## 1. Prepare without creating resources

```text
Load wodby2-deploy. Prepare a staging environment for app example in organization acme using the agreed stack
and source revision. Show the target cluster, required integrations, missing configuration, and resource costs.
Do not create resources or deploy yet. Ask about unresolved choices instead of guessing.
```

Expected result: resolved target resources and the preparation tool's outstanding questions. Review names and IDs,
not just labels such as "staging". Inspect the actual [environment configuration](../../apps/environments.md).

## 2. Authorize the reviewed operation

Approve the specific creation or deployment and required scopes. Creation tools require `confirm: true` reflecting
that approval. If a required integration or setting has no available tool, configure it in the dashboard and ask the
agent to prepare again. Do not broaden credentials just to bypass a missing tool.

Creating an app or environment may trigger builds and deployments. Record every returned task ID and follow
`suggestedCalls` until the related work is complete. See [builds](../../apps/builds.md) and
[deployments](../../apps/deploys.md).

## 3. Verify more than task completion

Ask the agent to report:

1. The deployed repository revision and stack revision.
2. Creation, build, and deployment outcomes, including warnings and failed steps.
3. Pod readiness and relevant application logs.
4. Database connectivity, uploads, and representative application behavior.
5. Whether workers, schedules, and outbound integrations remain isolated.

Authorize HTTP requests and other active checks before running them. A completed deployment is not proof that the
application behaves correctly. List untested checks explicitly.

## 4. Handle failure or an uncertain result

If a request times out, first inspect the target environment and recent tasks. Do not create another environment or
repeat an import blindly. Use the [troubleshooting walkthrough](troubleshoot.md), then request approval for the
proposed fix. Record any remaining paid resources if the rehearsal stops.

## 5. Hand off the result

Return the environment and task IDs, deployed revision, approved test results, warnings, and remaining decisions.
Production data imports, DNS changes, cutover, and cleanup are separate approvals. Successful staging does not
authorize production deployment or deleting the old hosting environment.
