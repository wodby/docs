---
description: Run the T3 Code server on Wodby with the T3 Code catalog stack, a web interface for the Codex, Claude Code and OpenCode coding agents.
---

# T3 Code

The Wodby T3 Code catalog stack runs the [T3 Code](https://github.com/pingdotgg/t3code) server, a web interface for the
Codex, Claude Code, and OpenCode coding agents. The agents run inside the app service's container and work on
repositories stored on its volume. The current composition is documented in
[`wodby/stack-t3code`](https://github.com/wodby/stack-t3code).

## Before you create the app

- The stack has one service, T3 Code, which runs one replica. T3 Code keeps its state in a single SQLite database, so
  it cannot be scaled out.
- The `data` volume is 20 GB by default. It holds your projects, agent sign-ins, and installed tools. Choose a size
  that fits them: a volume cannot be resized after it is created. See [Volumes](../../../apps/services.md#volumes-tab).
- The container requests 0.5 CPU and 1 GiB of memory and is limited to 4 CPU and 8 GiB. Raise the limits if your
  agents run large builds or test suites. See [Resources](../../../apps/services.md#resources-tab).
- The cluster needs outbound internet access. Claude Code is downloaded from Anthropic on the first start, and the
  agents call their model providers.

## Sign in

T3 Code has no password. Each browser or T3 Code app signs in once with a one-time pairing link, which expires after
5 minutes.

1. Deploy the app, then run the **Generate pairing link** action on the T3 Code app service. See
   [Actions](../../../apps/services.md#actions).
2. Open the link from the task log in the browser you want to sign in.

You can also run `t3-pairing-link` in a [web terminal](../../../apps/web-terminal.md).

The link points to the app's main domain as it was at the last deployment. After you change the main domain, deploy the
app service again. See [Main and primary](../../../apps/endpoints.md#main-and-primary). Without a main domain, you get
only a token: enter it on T3 Code's sign-in page.

T3 Code also prints a pairing link in the app service's log each time it starts. That link uses the container's internal
address, so enter its token on the sign-in page instead of opening it.

To list and revoke signed-in devices, run these commands in a web terminal:

```bash
t3 auth session list
t3 auth session revoke <id>
```

## Sign in to the agents

| Agent | Command | Where it comes from |
| --- | --- | --- |
| Codex | `codex` | included in the image |
| OpenCode | `opencode` | included in the image |
| Claude Code | `claude` | downloaded from Anthropic to the volume in the background on first start; updates itself |

None of the agents is signed in. Choose one of these ways:

- In T3 Code, open **Settings → Providers**.
- In a [web terminal](../../../apps/web-terminal.md), run `codex login`, `claude auth login`, or `opencode auth login`.
- Add API keys such as `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` as environment variables on the T3 Code app service, mark
  them as secret, and deploy. The agents inherit them. See [Secrets](../../../apps/environment-variables.md#secrets).
- Enter API keys per provider in T3 Code's settings.

Sign-ins made in T3 Code or the web terminal are stored on the volume and survive restarts.

## Work with repositories

Projects live in `~/projects` (`/data/projects`), the default working directory. Clone repositories there with `git`
in a web terminal. Git credentials, such as SSH keys in `~/.ssh`, are stored in the home directory on the volume.

To add another agent or a command-line tool, install it with `npm install -g` or into `~/.local/bin`. Both locations
are on the volume and take priority over the tools in the image.

## Agent permissions and sandboxing

New threads use **Full access**, T3 Code's default. Agents then run commands without asking for approval, and the
container is the only boundary. An agent can read everything in the container, including its environment variables and
the files on the volume. Keep credentials you do not want an agent to use out of the app service.

Codex's **Supervised** and **Auto** modes run commands in a sandbox that needs unprivileged user namespaces. If the
cluster blocks them, those commands fail with a `bwrap` error. Use **Full access** for that thread.

T3 Code's built-in browser downloads itself to the volume on first use and needs the same namespaces for Chrome's
sandbox. If a browser tab reports that the host blocks the sandbox, `t3 browser setup` cannot fix it inside the
container. Setting `T3CODE_SERVER_BROWSER_SANDBOX` to `0` runs the browser without Chrome's sandbox. A compromised web
page could then reach everything in the container.

## Who can reach it

The T3 Code domain is public. Anyone can open the sign-in page, but only a paired browser or app can do anything else.

- Treat a pairing link like a password until it is used or expires.
- A paired device can run agents with full access to the container. Revoke devices you no longer use.
- Anyone who can run the app service's actions or open its web terminal in Wodby can sign a new device in. So can anyone
  who reads its log within 5 minutes of a start. Limit those permissions to people who should use T3 Code.

## Change configuration

Change environment variables on the T3 Code app service, then deploy it. See
[Environment variables](../../../apps/environment-variables.md).

- `T3CODE_TELEMETRY_ENABLED` is `false`. Set it to `true` to send T3 Code's product usage data.
- T3 Code reads other `T3CODE_*` variables. Keep `T3CODE_HOST` unchanged and `T3CODE_PORT` set to `3773`. Without
  `T3CODE_PORT`, the server does not start.

Agent turns stream over a long-lived WebSocket connection. The domain's request timeouts are `0s` for this reason. Keep
them that way, and do not set `request_body_size` on the domain: the gateway then refuses WebSocket connections and T3
Code cannot connect. See [HTTP settings](../../../apps/endpoints.md#http-settings).

## Data

The `data` volume is mounted at `/data`, the home directory of the user T3 Code runs as. It holds T3 Code's database
(`~/.t3`), agent sign-ins, Git credentials, tools you install, and `~/projects`. Everything outside `/data` is reset
when the container restarts.

The T3 Code service has no backup or import operation in Wodby. Push your work to a Git remote: if the volume is lost,
every device and agent must sign in again and unpushed work is gone.

## Check the result

In a web terminal, run:

```bash
curl -fsS http://localhost:3773/.well-known/t3/environment
```

It reports the running version and needs no sign-in.
