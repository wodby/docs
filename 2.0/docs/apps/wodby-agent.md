# Wodby Agent

Wodby Agent is a coding agent built into [development workspaces](workspaces.md). You chat with it in the dashboard,
and it works in the workspace's Git checkout and runs commands in your SSH runner. You don't need SSH or an account
with a model provider. It uses the GLM 5.3 model and pays with your organization's
[AI credits](../pricing.md#ai-credits).

!!! note "Availability"
    Wodby Agent must be enabled in Wodby. When it isn't, the **Agent** tab shows only your
    [agent connections](../agents/permissions.md).

## Use Wodby Agent

1. Open the workspace environment's **Workspace** page, then **Agent**.
2. Keep **Wodby Agent** selected. It starts automatically while the environment is running.
3. Type your request and press Enter. Shift+Enter starts a new line.

Your first message starts a new chat, named after that message. Your chats are listed beside the open one: select one
to continue it, or select **New chat**. To interrupt the agent, select the stop button in the message box.

Only the workspace owner can use the agent. Chats are kept in the owner's private home in the workspace, so they
survive runner restarts and pauses.

Your messages, and the code and command output the agent reads, are sent through Wodby to the model provider to
generate responses.

## Approvals

The agent reads, searches and edits files in the checkout without asking. It asks before anything else, such as
running a command: select **Allow once** or **Reject**. Its file tools work only inside the checkout. When the agent
asks a question, choose an answer and select **Answer**.

Commands you allow run as the workspace user, with the same access as your SSH sessions, including pushing to the
app's repository.

Settings in the repository, such as `opencode.json`, don't change the agent's model or approvals. Plugins in the
repository's `.opencode/plugin` directory do run inside the agent and can use your AI credits, so use the agent only
with repositories you trust.

## AI credits

Every input, cached input and output token of a request counts against the organization's AI credits: first the
month's included tokens, then purchased tokens, then additional usage within the spending limit on paid plans. If
you can view billing, the **Agent** tab shows this month's usage below the message box.

When the credits run out, the agent stops until you buy tokens, raise the spending limit or the next month starts.
See [AI credits](../pricing.md#ai-credits).

## Other agents

To use another agent in the workspace, follow its steps on the workspace's **Connect** tab; see
[Connect your editor or agent](workspaces.md#connect-your-editor-or-agent). opencode run over SSH also uses AI credits,
with GLM 5.3 as its default model, unless you choose a model from your own provider. Claude Code, Codex and other
agents use your own provider account and aren't billed through AI credits.

The **Agent** tab also lists your [agent connections](../agents/permissions.md). Select one to see the tasks it ran in
the environment.
