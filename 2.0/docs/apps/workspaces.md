# Development workspaces

A development workspace is an app environment where you or a coding agent can edit a persistent Git checkout and test
changes against the running application. Commit and push the result, then build and deploy it in a separate CI/CD
environment.

!!! note "Availability"
    Workspace creation must be enabled in Wodby, and the selected stack and cluster must support it. If
    **Development workspace** is unavailable, hover over it to see why, or use **CI/CD**. A service that supports Git
    builds does not necessarily support workspaces.

<span id="workspace-or-standard"></span>

## Workspace or CI/CD?

| | Development workspace | CI/CD environment |
| --- | --- | --- |
| Application code | Editable Git checkout on persistent storage | Code delivered in a built container image |
| Updating code | Edit through SSH; reload or restart as the runtime requires | Build and deploy a new image |
| Git updates | Pull, commit and push explicitly from the checkout | Use the environment's configured CI/CD workflow |
| Purpose | Development and testing with your tools or agents | Reproducible staging and production deployments |

Choose the **Deployment mode** when creating an environment. You cannot switch an existing environment between modes.
The mode is separate from the [environment type](environment-types.md): selecting `dev` alone does not create a workspace.
In the API and MCP tools, CI/CD is the `STANDARD` execution mode and a development workspace is `WORKSPACE`.
App and environment lists mark workspaces with a **Workspace** tag.

A workspace belongs to the user who creates it. Only that owner, while retaining permission to modify the app, can
connect to its personal SSH runner or change workspace configuration. Normal resource-management permissions still
apply to pausing and deleting the environment.

## Before you create one

- Deploy to Wodby Cloud, or select an existing ready cluster that can publish a TCP endpoint for SSH. An existing
  cluster needs exactly one default storage class. See [Storage](#storage).
- Choose a stack with one supported source service. Any services that share its code, such as a web server, must also
  support workspace mounts.
- Use your own Git repository, so you can push your work. Connect an existing repository, or clone the service's
  boilerplate into a new repository with a [GitHub](../providers/github.md) or [GitLab](../providers/gitlab.md)
  integration.
- Add your public key in [User settings > SSH keys](../user/ssh-keys.md). Keep the private key on your computer. Until
  you add one, the app form and the **Workspace** page warn you and link to that page. A key you add later works
  without restarting the workspace.
- Start with fresh application data. Attaching an existing database or selecting a data import during workspace
  creation is not supported.

The SSH runner uses additional compute and counts toward service usage. Its resource allocation matches the source
service. Code and agent-home storage are also billed under normal storage rules.

## Create a workspace

1. Start creating an app, or add an environment from `Apps > [App] > Environments`.
2. Select the stack, then deploy to Wodby Cloud or select an existing cluster.
3. In the app settings, set **Deployment mode** to **Development workspace**. If the option is unavailable, hover over
   it to see why.
4. In the services step, open the **Development workspace** section. For the source service, choose
   **Clone boilerplate** to create a new repository from the boilerplate, or **Use my repository** and select the
   repository and the Git reference to start from.
5. Optionally, change **Code, size (Gi)** and **Agent home, size (Gi)** in the **Workspace** group under **Volumes**.
6. Review the services, resource usage and access settings, then create the environment.

Wodby starts a new working branch named `wodby/workspace-<id>` from the starting reference. The
**Development workspace** section shows its name. Commit and push your work to this branch, then open a pull request.

Wodby clones the selected source once, runs the source service's setup steps, such as installing dependencies, then
starts the code services. Open the environment's **Workspace** page to follow **Setup** and view participating
services. **Setup steps** lists the steps in the order they run; select one to view its command. If setup fails, check
the environment's task logs.

The page also shows the checkout's live **Git status**: the current branch and whether it is pushed, the latest commit,
and the uncommitted changes. Select **Refresh** to read it again. Only the workspace owner sees it. The initial branch
and commit on the page record the state at creation.

### Storage

Wodby keeps the code checkout and agent home on volumes of the cluster's default storage class, and runs the code
services, the SSH runner and setup jobs on the same node. Any storage class works; it doesn't need to support
shared access across nodes. A new Wodby Cloud cluster always has a default class. On an existing cluster, the
**Development workspace** option stays unavailable until the cluster has exactly one default storage class.

When you create a workspace through the [API](../dev/api.md) or [MCP](../dev/mcp.md), you can choose another storage
class of an existing cluster instead, or an enabled storage service from the stack that shares the files across nodes.
Network storage is usually slower, and file watchers may need polling.

You cannot change the storage after creating the workspace.

## Connect your editor or agent

1. As the owner, open **Workspace**, then **Connect**.
2. Copy the supplied SSH configuration into `~/.ssh/config` and replace `YOUR_PRIVATE_KEY` with your private-key filename.
   The host is named `wodby-workspace-<app>-<environment>`, the same name that MCP returns.
3. Run the supplied SSH command and compare the server fingerprint with the one shown in Wodby before accepting it.
4. Open the working directory shown in the connection details.

The **Connect** panel includes steps for common tools:

- **VS Code or Cursor**: install the Remote - SSH extension, run **Remote-SSH: Connect to Host…**, choose the workspace
  host and open the working directory.
- **Claude Code**: run `claude` in the working directory and sign in with your own account. The first run downloads
  Claude Code from Anthropic into your private home. To continue the session from the Claude app, run
  `claude remote-control` in a persistent terminal session, such as tmux, and open the URL it prints. Remote Control
  requires an eligible account.
- **Codex**: sign in with `codex login`, or `codex login --device-auth` without a browser, then add the SSH host in the
  Codex app under **Settings → Connections**.
- **opencode**: run `opencode` in the working directory and sign in to your model provider with `opencode auth login`.
- **Hermes Agent**: it runs on your computer. Set its terminal backend to `ssh`, with the workspace host and the user
  from the connection details.

Claude Code, Codex and opencode come with the workspace, so you only sign in. They update with Wodby and don't update
themselves; to manage versions yourself, install your own copy and put it first on your `PATH`. Claude Code and
opencode need an Alpine-based runtime image, which Wodby's services use; on other images, install them yourself. A
workspace created earlier gets these tools after **Restart SSH runner**.

Any other tool that works over SSH can use the workspace too. Install and authenticate it as its provider requires.
Wodby does not include a built-in dashboard coding agent.

Agent tools and credentials stored in your private home persist across runner restarts and pauses. Application
containers do not share that home. The agent can access the application's code and environment through the runner;
use credentials and application data appropriate for development.

`git push` and `git fetch` for the app's repository use the app's Git integration, so you don't set up Git credentials
for it. Wodby renews the short-lived credential automatically. It removes the credential while the workspace is paused
and when you lose access to the app or to the integration.

- With GitHub, the credential only reaches the app's repository.
- With GitLab and Bitbucket, it has the integration's access to your provider. A GitLab access token without write
  access can't push.
- Pushes use the integration's identity; commits keep the author from your Git configuration.
- For other repositories, add your own credentials.
- A workspace created earlier gets this after **Restart SSH runner**.

Do not commit agent credentials or Git tokens. Coordinate multiple agents using the same checkout; they can otherwise
overwrite each other's edits.

Updating your registered SSH keys refreshes workspace access and ends existing runner sessions. Removing permission
to modify the app also removes owner access. Revocation can be delayed if the cluster is unreachable.

### MCP controls

[Connect your client to Wodby MCP](../dev/mcp.md) to inspect workspace state and manage its lifecycle. Discover available
tools from the connected server before using them.

| Tool | What it does |
| --- | --- |
| `get_workspace_context` | Reads runtime and preview information, setup state and initial Git details. |
| `get_workspace_connection` | Returns the owner's SSH connection details, the agents ready in the workspace and connection guidance. |
| `prepare_workspace` | Reruns setup while preserving the checkout. |
| `restart_workspace` | Restarts the SSH runner and ends active sessions. It does not restart the application. |
| `pause_workspace` / `resume_workspace` | Pauses or resumes the environment. |

Read tools require `mcp:read` with OAuth. Lifecycle tools require `mcp:operate` and `confirm: true` reflecting your
approval; follow the returned task to completion. The `develop_in_workspace` prompt, when offered by your client,
guides the workflow but does not authorize operations.

Connecting MCP does not connect your editor to SSH or move an existing agent session into the workspace. Workspace
MCP tools do not edit files or report live Git status. Establish the remote connection separately.

## Edit, reload and rerun setup

Edits affect this environment's shared checkout. Whether a browser preview updates immediately depends on the service
and your application. PHP can read changed source on subsequent requests, but application caches may need clearing.
File watchers usually work. If the workspace uses a storage service, development servers need a watcher that works
with network storage; custom Node commands may require polling.

Use **Restart application** when the runtime does not reload changes. This preserves the checkout and does not pull
Git updates or reinstall dependencies. **Restart SSH runner** only restarts your remote connection service and ends
SSH and agent sessions.

To restart other services, for example after changing a database setting, create a deployment from **Deploys**. In a
workspace, a deployment restarts the selected services from the checkout, without builds or post-deployment scripts.

Use **Retry setup** after correcting a failed setup or when dependencies need installing again. It stops code services
while the setup steps run; supporting services and an available SSH runner remain usable. Setup may change
dependencies and generated files, so review your Git diff afterward. It never pulls, resets or reclones an initialized
checkout.

Workspace setup is separate from ordinary post-deployment scripts. Those scripts do not run for workspace deployments.
After pulling code yourself, decide whether to rerun setup, run an application-specific command, or restart the
application.

For Drupal projects with a tracked settings file, include the required Wodby settings bootstrap intentionally in your
project. Setup will not rewrite tracked settings or replace tracked upload placeholders. Making a tracked file
ignored does not remove it from Git.

## Deliver changes to a CI/CD environment

1. Inspect the current branch and diff inside the workspace. Run the project's tests and check its preview.
2. Commit the intended source changes and push them to your Git provider.
3. Open a pull request and complete your normal review process.
4. Build and deploy the approved code in a separate CI/CD environment using your usual [CI/CD](../cicd/index.md).

Workspaces use development images and tools. A successful workspace preview does not prove the production image will
build or run; the CI/CD environment's build and tests validate that. Local dependency installations, uncommitted
files and workspace data are not transferred with a Git push. Wodby does not automatically create a PR or a preview
environment as part of this workflow.

## Limits and recovery

- Code services run one replica without autoscaling. Scheduled jobs remain disabled.
- Code-service derivatives must be disabled; supporting-service derivatives can remain available.
- Changing the repository, source links or storage, upgrading the stack, deploying a built image into the workspace, and
  moving it to another cluster are not supported. Create a new environment for those changes.
- The code services, the SSH runner and setup jobs run on one node, so that node needs room for all of them.
  With node-local storage, such as the default K3S storage class, the workspace can only run on the node that holds
  its volumes.
- To protect HTTP previews with [App Access](access.md), choose **Selected endpoints**. **Entire app** protection
  conflicts with the workspace's published SSH port. HTTP access policies do not protect that SSH endpoint.
- [Pausing](environments.md#pausing-and-resuming-an-environment) stops workloads and SSH access but preserves code and
  agent-home storage. Storage remains provisioned and billable; pausing does not delete the cluster.
- Resume does not pull code. It can retry setup interrupted by a lifecycle operation, but an ordinary setup failure
  requires an explicit retry after you fix the cause.
- Failed setup leaves code services stopped. If the SSH runner is ready, connect to inspect and repair the checkout,
  then retry setup. A missing or inconsistent checkout needs recovery rather than an automatic reclone.

Before deleting the environment, push any work you need and copy out important local data or agent settings.
Persistent workspace storage is not a substitute for keeping your source in Git.
