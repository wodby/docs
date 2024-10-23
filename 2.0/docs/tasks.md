# Tasks

All operations in Wodby 2 normally executed as tasks for security and recording. Our approach is we want to be transparent with what has been done with your infrastructure. Tasks performed by support team will be displayed among with users' tasks. The support member will have `support` role in your organization that limits him/her to certain actions.

## Jobs and steps

Similar to Wodby CI pipeline format tasks consist of jobs that consist of steps. Jobs can run in parallel, steps always executed sequentially. We show the sequence of jobs execution in a task's graph in Wodby dashboard. A task job's step may provide logs.

## Information

A task has the following information:

- Task status, values could  `done`, `failed`, `done with warnings`, `timed out`, `in progress`, `queued`, `pending`, `backed off`, `canceling` and `canceled`
- Author. A user who run a task. Automated tasks usually authored by `Wodbot`. Tasks performed by `Superadmin` are usually manual technical actions by Support team but mostly actions performed via Wodby dashboard will show the exact user with `support` role in your organization
- Duration. Most of the executable tasks have a certain hard timeout, when timeout reached and the task not finished, it will be marked as `timed out`
- Project. If a task was executed in context of an in-project entity, such as an app or a kubernetes cluster, the related project will be linked to the task. When it's an organization-level task though there will be no project associated.

## Types

There are two types of tasks:

1. Immediate task. Such tasks are simple actions that created simply to keep the history of actions, such as a user added to project.
2. Executable tasks, such task have a duration and often have logs

## Rerun task

Failed tasks can be re-run. A new task copy will be created and executed. Some tasks such as build and deployment task will create a new build/deployment when a task re-run. Some tasks are not allowed to re-run.

### Forced re-run

Optionally, you can rerun tasks with forced flag, such tasks if occur a _user error_ (not unexpected system error) will treat such errors as warnings and if it had warnings it will have `done with warnings` status upon completion.

## Origin task

Some tasks may not be produced by users but produced by other tasks, for example application creation task will always produce a deployment (and sometimes build) task. 

## Silent task

You may notice that some tasks may not appear in the Wodby dashboard's tasks widget, such immediate tasks considered silent and will be quietly added to the record without disturbing you.

## System jobs and steps

Rarely, if a task fails but none of the associated jobs or steps seems to fail it may mean that there's a system job or step that failed. In such cases please [contact us](support.md).
