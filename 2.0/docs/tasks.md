# Tasks

Most operations in Wodby run as tasks.

Tasks give you an audit trail for changes to your infrastructure and product resources. User actions, automated actions, and support actions can all appear in task history, so you can see what happened and when.

## Jobs and steps

Tasks are divided into jobs, and jobs are divided into steps.

Jobs can run in parallel. Steps inside a single job always run sequentially. The dashboard shows the execution graph for task jobs, and steps may include logs when the underlying operation produces them.

## Information

A task has the following information:

- status: `done`, `failed`, `done with warnings`, `timed out`, `in progress`, `queued`, `pending`, `backed off`, `canceling`, or `canceled`
- author: the user or system actor that triggered the task. Automated tasks are usually authored by `Wodbot`. Support-initiated tasks appear with a support-scoped user where applicable.
- duration: executable tasks have a runtime and may be stopped by a hard timeout
- project: tasks linked to project-scoped resources such as apps or clusters show the related project. Organization-level tasks do not.

## Types

There are two types of tasks:

1. Immediate tasks. These are simple record-only actions, such as adding a user to a project.
2. Executable tasks. These tasks take time to run and often include logs.

## Rerun task

Failed tasks can sometimes be rerun. Wodby creates a new task and executes it again. For build- and deployment-related tasks, rerunning usually creates a new build or deployment rather than resuming the old one.

Some task types cannot be rerun.

### Forced re-run

You can optionally force a rerun. In that mode, user-facing errors are treated as warnings instead of hard failures, and the task may finish with `done with warnings`.

## Origin task

Some tasks are created by other tasks rather than directly by a user. For example, creating an app usually triggers a deployment task, and sometimes a build task as well.

## Silent task

Some immediate tasks are silent. They are still recorded, but they may not appear in the main tasks widget because they are not important enough to interrupt the normal activity stream.

## System jobs and steps

Rarely, a task can fail because of an internal system job or step that is not shown in the regular task graph. If that happens, [contact support](support.md).
