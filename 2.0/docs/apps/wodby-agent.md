# Wodby Agent

Wodby Agent is the assistant built into Wodby. You chat with it in the dashboard, in two places:

- In a [development workspace](workspaces.md) it is a coding agent: it works in the workspace's Git checkout and
  runs commands in your SSH runner. See [Use Wodby Agent](#use-wodby-agent).
- In an organization's **Chats** it works across the organization with Wodby's own tools: it deploys and configures
  apps, reads logs and tasks, and explains what went wrong. See [Organization chats](#organization-chats).

You don't need SSH or an account with a model provider. It pays with your organization's
[AI credits](../pricing.md#ai-credits).

!!! note "Availability"
    Wodby Agent must be enabled in Wodby. When it isn't, the **Chats** tab shows only your
    [agent connections](../agents/permissions.md).

## Use Wodby Agent

1. Open the workspace environment's **Workspace** page, then **Chats**.
2. Keep **Wodby Agent** selected. It starts automatically while the environment is running.
3. Type your request and press Enter. Shift+Enter starts a new line.

Your first message starts a new chat, named after that message. Your chats are listed beside the open one: select one
to continue it, or select **New chat**. To interrupt the agent, select the stop button in the message box.

Only the workspace owner can use the agent. Chats are kept in the owner's private home in the workspace, so they
survive runner restarts and pauses.

The agent sends the whole chat with every request, so a longer chat uses more AI credits for each step. **Context**,
below the message box, shows how full the chat is. When it fills up, the agent summarizes the earlier conversation
and carries on; the summary stays in the chat, collapsed. Start a new chat for a new task to keep it small.

Your messages, and the code and command output the agent reads, are sent through Wodby to the model provider to
generate responses. Wodby Agent currently runs on the GLM 5.3 model, which may change.

## Approvals

The agent reads, searches and edits files in the checkout without asking, and its file tools work only inside the
checkout. Choose what else it asks you to approve in the **Approvals** list next to the model:

- **Ask before pushing** (the default): commands and changes to the environment run without asking, except pushing
  to a Git remote.
- **Ask before commands**: every command, web request and change to the environment asks.
- **Never ask**: nothing asks.

Changing the setting restarts the agent, which stops a running chat. When the agent asks, select **Allow once** or
**Reject**. When it asks a question, choose an answer and select **Answer**.

Commands run as the workspace user, with the same access as your SSH sessions, including pushing to the app's
repository. **Ask before pushing** recognizes pushes in the command text only, so it misses a push inside a script
or an alias, and a repository's own `opencode.json` can turn it off. For a repository you don't fully trust, choose
**Ask before commands**. Repository settings don't change the agent's model. Plugins in the repository's
`.opencode/plugin` directory do run inside the agent and can use your AI credits, so use the agent only with
repositories you trust.

## Working with the environment

The agent can also work with the workspace environment itself, with your access:

- check its services, logs, deployments and tasks
- deploy it, and run service actions and cron jobs
- enable or disable its services, except the ones that hold your code
- run commands in its containers, for example to clear a cache. This needs a paid plan, like the
  [web terminal](web-terminal.md).

These changes ask for approval only when you chose **Ask before commands**. The agent can't reach your other
environments or apps, change other settings or delete anything.

## What the agent knows about your services

Wodby already connects an application to the services around it: a linked database, cache, search or mail service
reaches the code as environment variables, and some services generate settings files. Each service describes what it
sets up, and the agent reads that before it changes how an application is configured. For example, on a Drupal
environment it knows that the settings file is generated and what the Redis cache still needs, so it does not add a
second configuration to your code.

Services you write yourself can describe themselves the same way. See
[`guidance`](../services/template.md#guidance) in the service template.

## Organization chats

Open **Chats** in the organization's menu, type a request and press Enter. Every member has their own chats; nobody
else sees them. The agent acts for you in that organization only, with your access: it can do what you can do, and no
more.

What you can ask for:

- Create an app from a stack, deploy it, and follow builds, deployments and tasks.
- Change an environment: variables, CPU and memory, replicas, cron schedules, routes, pausing and maintenance mode.
- Set up and take backups, including to Wodby Blob.
- Review an environment or the whole organization and say what is unhealthy, unprotected or out of date.
- Find out why a build, deployment or task failed. A failed task's page has a button to ask Wodby Agent about the
  failure, which starts a chat about that task.
- Read files in a connected Git repository, commit files to it, and create a repository through a Git integration.
  Commits the agent makes are authored by Wodby Agent.
- Answer questions from these docs.

### What it asks first

The agent reads on its own. Anything that changes something waits for you:

- The chat shows what the agent wants to do and what it acts on, by name. Select **Approve** or **Decline**.
- An action that deletes, overwrites, upgrades or interrupts something, or runs a command in a container, is shown in
  red and asks a second time before it runs. Approve it only if you asked for exactly that.
- When the agent needs a choice from you, it asks a question with the answers to pick from. Choose one, or type your
  own under **Other**, and select **Answer**.

While a chat waits for you it takes no new message. Select the stop button to end the run instead.

### What it won't do

- It can't set or reveal a secret, such as a database user's password. It tells you where in the dashboard to do it.
  Don't paste passwords, keys or tokens into a chat: a chat keeps what is written in it.
- It can't act outside the organization the chat belongs to.
- Running a command in a container needs a paid plan, like the [web terminal](web-terminal.md).

Organization chats use AI credits the same way as workspace chats.

## AI credits

Every input, cached input and output token of a request counts against the organization's AI credits: first the
free tokens it gets once, then purchased tokens, then additional usage within the spending limit on paid plans. If
you can view billing, the **Chats** tab shows the free and purchased tokens left below the message box.

When the credits run out, the agent stops until you buy tokens, upgrade or raise the spending limit.
See [AI credits](../pricing.md#ai-credits).

## Other agents

To use another agent in the workspace, follow its steps on the workspace's **Connect** tab; see
[Connect your editor or agent](workspaces.md#connect-your-editor-or-agent). opencode run over SSH also uses AI credits,
unless you choose a model from your own provider. Claude Code, Codex and other agents use your own provider account
and aren't billed through AI credits.

The **Chats** tab also lists your [agent connections](../agents/permissions.md). Select one to see the tasks it ran in
the environment.
