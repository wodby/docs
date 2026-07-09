# Create a stack

A stack is the blueprint used to create an app. It selects the [services](../services/index.md) an app uses and defines
the default configuration for those services.

Create or import the services you need before creating a custom stack. See [Create a service](../services/create.md).

## Choose a creation method

Use the method that matches how you want to manage the stack:

| Method | Use when |
| --- | --- |
| Dashboard catalog | You want to copy an existing public Wodby stack and customize it. |
| Dashboard from scratch | You want to choose services and defaults in the dashboard. |
| Duplicate stack | You want an independent copy of an existing owned stack. |
| Dashboard Git import | You maintain `stack.yml` in a Git repository and want Wodby to track that repository. |
| CLI Git import | You want the same Git-backed stack import from automation or scripts. |
| CLI manifest creation | You have a local `stack.yml` and want to create a non-Git-backed stack. |
| Helm scaffold | You want to generate a starter service and one-service stack from a simple Helm chart. |

## Add a catalog stack

Use a catalog stack when an existing public Wodby stack is close to what you need.

1. Open `Stacks`.
2. Select a public catalog stack.
3. Use `Add stack` to copy it into your organization or project.
4. Review the add form before creating it.

The copied stack can be customized and deployed like any other stack. It keeps an origin, so you can later
[sync catalog changes](updates.md#sync-with-origin). The add form lets you decide whether `Services auto update` and
`Auto sync with origin` start enabled.

## Create a stack from scratch

Use the dashboard when you want to assemble the stack interactively.

1. Open `Stacks`.
2. Create a new stack.
3. Add stack services from available service revisions.
4. Configure required services, main service, replicas, options, links, volumes, settings, env vars, tokens, configs,
   Helm values, and resource defaults as needed.
5. Publish the draft revision.

See [Stack configuration](configuration.md) for the available stack and stack-service settings.

## Duplicate a stack

Use `Duplicate stack` on an owned stack when you need an independent copy.

The duplicate is not linked to the original stack. Later changes to one stack do not change the other. If you duplicate
a Git-backed stack, the duplicate is created as a regular dashboard-managed stack and does not stay linked to the Git
repository.

## Import a Git-backed stack

Use Git when you want the stack manifest to remain the source of truth.

The repository must contain a `stack.yml`, or an `index.yml` that lists multiple stack directories:

```yaml
stacks:
  - php
  - node
```

Each listed directory must contain its own `stack.yml`. See the [stack template reference](template.md).

### Dashboard

1. Connect a Git provider integration if the repository is not already available. See [Git provider](../providers/git.md).
2. Open `Stacks`.
3. Start an import from Git.
4. Select the organization or project, Git integration, repository, ref type, and ref.
5. Import the stack.

Git-backed stacks can later be updated from the same repository manually or automatically. See [Stack updates](updates.md).

### CLI

Use `wodby stack import` for a Git-backed stack:

```bash
wodby stack import \
  --org 123 \
  --integration github-main \
  --remote-git-repo acme/custom-stacks \
  --git-ref main \
  --git-ref-type branch \
  --wait
```

To create the stack in a project scope, include `--project`:

```bash
wodby stack import \
  --org 123 \
  --project 456 \
  --integration github-main \
  --remote-git-repo acme/custom-stacks \
  --git-ref v1.0.0 \
  --git-ref-type tag \
  --wait
```

See [`wodby stack import`](../cli/wodby_stack_import.html) for all flags.

## Create from a local manifest

Use manifest creation when you have a `stack.yml` file and do not need Wodby to track a Git repository.

Validate the manifest first:

```bash
wodby stack validate-manifest stack.yml --org 123
```

Create the stack:

```bash
wodby stack create-from-manifest stack.yml --org 123 --version 1.0.0
```

Create it in a project scope:

```bash
wodby stack create-from-manifest stack.yml --org 123 --project 456 --version 1.0.0
```

Use `--include` for referenced files such as stack configs when the manifest points to local files:

```bash
wodby stack create-from-manifest stack.yml \
  --org 123 \
  --version 1.0.0 \
  --include configs/php.ini
```

See:

- [`wodby stack validate-manifest`](../cli/wodby_stack_validate-manifest.html)
- [`wodby stack create-from-manifest`](../cli/wodby_stack_create-from-manifest.html)

## Create from a Helm scaffold

Use the Helm scaffold workflow when a chart represents one logical service and you want a minimal stack for deploying it.
The Wodby CLI can generate both a service manifest and a one-service stack manifest:

```bash
wodby helm scaffold-stack \
  oci://registry-1.docker.io/bitnamicharts/memcached \
  --version 8.6.9 \
  --service-out service.yml \
  --stack-out stack.yml
```

If the chart needs non-default values to render the right workload shape, pass them during scaffolding:

```bash
wodby helm scaffold-stack \
  oci://registry-1.docker.io/bitnamicharts/memcached \
  --version 8.6.9 \
  --values-yaml values.yml \
  --service-out service.yml \
  --stack-out stack.yml
```

Create the generated service first:

```bash
wodby service validate-manifest service.yml --org 123
wodby service create-from-manifest service.yml --org 123 --version 1.0.0
```

Then create the generated stack:

```bash
wodby stack validate-manifest stack.yml --org 123
wodby stack create-from-manifest stack.yml --org 123 --version 1.0.0
```

The generated stack is intentionally minimal. Review stack-service defaults such as options, Helm values, settings,
volumes, links, env vars, resource limits, and whether the service should be required or main before using it for apps.

For service-level chart inspection and generated `service.yml` details, see
[Create from a Helm chart](../services/create.md#create-from-a-helm-chart).

See [`wodby helm scaffold-stack`](../cli/wodby_helm_scaffold-stack.html) for all flags.

## After creating the stack

Use the stack to create an app or an app instance.

If you created a dashboard-managed stack, publish the draft before using it in apps. If you imported or created a stack
from a manifest, Wodby creates a versioned stack revision from that manifest.

When the stack changes later, app instances using older revisions can be upgraded. See [Application stack](../apps/stack.md)
and [Stack updates](updates.md).
