# Assess and plan a migration

Use this walkthrough for an application running outside Wodby. Moving an existing Wodby environment between clusters
is a different operation: see [App environment cluster migration](../../apps/migration.md).

## Requirements

- Give the agent access to the source repository through its host. Inspect configuration without executing unknown
  project scripts. Do not include secret values in the assessment.
- Identify the source environment, target organization, and which external services you want to keep.
- Decide whether this job is a read-only plan, a staging rehearsal, or production cutover. Each stage needs its own
  authorization. Repository access is not permission to connect to production.
- Connect Wodby with read access if you want the plan to use existing account resources. Without it, the agent can
  assess the repository but must leave target resources and compatibility checks unresolved.

## 1. Inventory the application

```text
Use wodby2-migrate to assess this repository for Wodby 2. Identify runtimes, build and start commands, workers,
schedules, databases, persistent files, external integrations, and secret names. Do not print secret values.
Do not execute scripts, access the current host, or change anything. Mark missing evidence as unknown.
```

Expected result: a component inventory with file references and unresolved questions. Include database extensions,
data format/version compatibility, build-time versus runtime configuration, and application migration commands.
Measure data size and capacity separately when authorized; do not turn guesses into downtime or cost promises.

## 2. Map components to Wodby

Have the agent compare available stacks and exact service revisions with the inventory. Prefer compatible existing
definitions. Use contract inspection tools and read-only creation preparation to identify required choices.

A successful preparation validates creation inputs, not application compatibility or data portability. Keep the
existing application; do not replace it with a starter boilerplate merely to make deployment easier.

## 3. Review the plan

Require a plan containing:

- source component, proposed Wodby service or retained dependency, compatibility evidence, and application changes
- target organization/project/environment, stack revision, cluster choice, integration needs, and secret names
- staging isolation, data-transfer method, application checks, and who performs unsupported steps
- provisioning costs, downtime assumptions, production cutover, backup/restore procedure, and rollback limits
- blockers and the next specific action requiring approval

The output is a plan, not a completed or validated migration. Missing host, DNS, or integration access must remain an
explicit handoff, not a reason to improvise credentials or remote commands.

## 4. Rehearse separately

After approving the destination, costs, code changes, and any data transfer, follow
[Deploy and verify staging](staging.md). Keep production hosting and DNS unchanged. Isolate queues, databases,
storage writes, email, webhooks, workers, and scheduled jobs so staging cannot act on production data.

Prefer synthetic or sanitized data. Production copies require explicit authorization and a restricted transfer path.
Review [imports](../../apps/imports.md) before overwriting data. An import may not be transactional, and restoring one
service does not guarantee a consistent rollback across the whole application.

## 5. Approve cutover only after verification

Review the exact data and routing changes, maintenance window, acceptance checks, and rollback decision deadline.
Establish backups, stop or drain writers as necessary, perform a consistent final transfer, and ensure there is only
one active set of production workers and schedules. Approve each unsupported operation for the responsible person
or system to perform.

Keep the source intact for the agreed recovery period. After the destination accepts writes, reversing DNS alone
does not reconcile divergent databases or files. If reverse synchronization is unproven, stop for a recovery decision
instead of switching back blindly. Deleting the source is a separate authorization.

## Preserve a checkpoint

Record the approved scope, source revision, resolved target IDs, task/build/deployment/import IDs, verification
results, and remaining decisions. Omit secrets and signed download URLs. After a timeout, inspect existing resources
and tasks before retrying; the original operation may have started.
