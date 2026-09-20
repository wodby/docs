# Skills and compatibility

Wodby skills describe multi-step workflows. MCP tools perform individual operations. A skill does not replace tool
permissions, user approval, or checking the connected server's current input schemas.

## Choose a workflow

| Skill | Use |
| --- | --- |
| `wodby2-get-started` | Assess fit and prerequisites, select resources, and choose the next workflow. |
| `wodby2-migrate` | Plan a move from another host, rehearse on staging, and separate production cutover approval. |
| `wodby2-deploy` | Prepare a deployment, follow tasks, and verify runtime state. |
| `wodby2-troubleshoot` | Diagnose failures with task logs, application logs, pod status, and metrics. |
| `wodby2-service` | Reuse or author and validate a service definition. |
| `wodby2-stack` | Compose services into a stack and validate it. |
| `wodby2-provider` | Reuse an integration contract or validate a custom variable-provider manifest. |

Provider authoring does not implement a new OAuth or infrastructure provider. Validation does not publish a manifest.
Missing integration setup may require a dashboard handoff.

## Use guidance without installing anything

After connecting, ask the agent to call `get_wodby_guidance` and load the skill for the job. For example:

```text
Load wodby2-migrate from Wodby guidance and assess this repository. Return a read-only migration plan.
Do not access the current host, create resources, transfer data, or change DNS.
```

The [migration walkthrough](workflows/migrate.md) explains the expected output and next decisions without requiring
you to read skill source files.

## Optional local installation

The [public skill distribution](https://mcp.wodby.com/agent-skills) provides a versioned JSON index, individual
`SKILL.md` files, and a downloadable archive. Download the archive linked from that index, inspect it, and extract it.
Load it using your host's supported local-plugin or skill installation mechanism. It contains portable skill
directories, a Codex-compatible plugin manifest, and HTTP MCP configuration; not every client accepts that plugin
format. Configure MCP separately when necessary.

Install from one source to avoid conflicting copies. Installing files neither connects an account nor authorizes
operations. If the client cannot install skills, use `get_wodby_guidance` instead.

## Versions and upgrades

Three versions have different meanings:

- The skill bundle version identifies workflow text and packaged files.
- The server implementation version identifies a Wodby MCP release.
- The MCP protocol version is negotiated between client and server.

They do not need to match. A newer bundle does not mean every server or client exposes every feature mentioned in it.
Always discover available tools and read their schemas before execution. If a tool is unavailable, report the gap and
use a documented fallback or a human handoff; do not invent a replacement operation.

For reproducible jobs, retain the versioned index URL and each skill's SHA-256 hash. Review changes before replacing
a pinned bundle. Use the public distribution to discover the current version rather than assuming an old link is
latest. These workflows target Wodby 2 only.

## Reuse maintained definitions

Prefer existing [services](../services/index.md) and [stacks](../stacks/index.md) when they fit. The
`get_service_contract` and `get_stack_contract` tools inspect revision-specific metadata, including service
composition and configuration requirements. They omit configuration values and are not editable manifests.

Wodby-maintained definitions can continue receiving [stack updates](../stacks/updates.md). Running environments
upgrade separately according to their [auto-upgrade settings](../apps/stack.md#auto-upgrade). Using an agent does not
remove the need to review production upgrades or maintain your application code and custom definitions.
