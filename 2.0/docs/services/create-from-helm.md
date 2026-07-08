# Create a service from a Helm chart

You can create a custom Wodby service from an existing Helm chart without putting the service manifest in Git first.
The Helm scaffold command renders the chart, detects workloads and Kubernetes Services, and generates a `service.yml`
that you can review, edit, validate, and create in your organization.

Use this workflow for charts that mostly represent one logical service, such as Memcached, Redis, a web server, or a
single application workload. If the chart installs several independent application components, CRDs, operators, or
cluster-scoped infrastructure, review whether it should become a [stack](../stacks/index.md) or an
[`infrastructure` service](types.md#infrastructure) instead.

## Requirements

- Wodby CLI installed and authenticated. See [Wodby CLI](../dev/cli.md).
- Access to create services in the target organization or project.
- A Helm chart reference that Wodby can render. This can be an OCI chart reference, a chart repository plus chart name,
  or a repository/chart URL shorthand.

## Inspect the chart

Start by inspecting the chart. This shows what Wodby can detect before it generates a manifest.

```bash
wodby helm inspect oci://registry-1.docker.io/bitnamicharts/memcached
```

You can also use repository/chart URL shorthand:

```bash
wodby helm inspect https://charts.bitnami.com/bitnami/redis
```

That shorthand is equivalent to:

```bash
wodby helm inspect --source https://charts.bitnami.com/bitnami --chart redis
```

Use `--version` when you want a specific chart version:

```bash
wodby helm inspect oci://registry-1.docker.io/bitnamicharts/memcached --version 8.6.9
```

Review warnings carefully. Warnings about multiple workloads, CRDs, hooks, persistent volume claims, or cluster-scoped
resources usually mean the generated manifest needs manual changes before it is safe to create as a Wodby service.

## Generate `service.yml`

Generate a service manifest and write it to a file:

```bash
wodby helm scaffold-service \
  oci://registry-1.docker.io/bitnamicharts/memcached \
  --version 8.6.9 \
  --out service.yml
```

You can override generated service metadata:

```bash
wodby helm scaffold-service \
  https://charts.bitnami.com/bitnami/redis \
  --version 22.0.7 \
  --service-name redis \
  --service-title Redis \
  --out service.yml
```

If the chart needs non-default values to render the right workload shape, pass them during scaffolding:

```bash
wodby helm scaffold-service \
  oci://registry-1.docker.io/bitnamicharts/memcached \
  --values-yaml values.yml \
  --out service.yml
```

The generated manifest is a starting point. Wodby can infer common parts of the service, but it cannot always know the
right service type, settings, links, volumes, backup behavior, tokens, or app-level configuration model.

## Review the generated manifest

A simple chart usually generates a manifest like this:

```yaml
name: memcached
title: Memcached
type: service
scalable: true

options:
  - version: 8.6.9
    tag: latest
    default: true

helm:
  name: memcached
  source: oci://registry-1.docker.io/bitnamicharts/memcached
  chart: oci://registry-1.docker.io/bitnamicharts/memcached
  version: 8.6.9

workloads:
  - name: memcached
    kind: deployment
    primary: true
    selector:
      matchLabels:
        app.kubernetes.io/instance: "{{helm.release}}"
        app.kubernetes.io/name: memcached
    containers:
      - name: memcached
        image: registry-1.docker.io/bitnami/memcached

endpoints:
  - name: memcached
    main: true
    ports:
      - name: memcache
        number: 11211
        main: true
        protocol: tcp
```

Important fields to check:

- `name`: stable machine name for the Wodby service.
- `type`: service type. Change it when the chart is a datastore, database, storage, or infrastructure service.
- `options[].version`: Wodby service option shown to users.
- `options[].tag`: container image tag appended to `workloads[].containers[].image`.
- `helm.source`, `helm.chart`, `helm.version`: chart reference Wodby uses for validation and deployment.
- `workloads[].selector.matchLabels`: must match exactly one rendered Kubernetes workload.
- `endpoints[]`: ports Wodby exposes for stack and app-service configuration.

For full manifest details, see the [service template reference](template.md).

## Validate and create the service

Validate the manifest before creating anything:

```bash
wodby service validate-manifest service.yml --org 123
```

Fix any validation errors in `service.yml`, then create the service:

```bash
wodby service create-from-manifest service.yml --org 123 --version 8.6.9
```

To create the service in a project instead of only at organization scope, pass `--project`:

```bash
wodby service create-from-manifest service.yml --org 123 --project 456 --version 8.6.9
```

After the service is created, add it to a stack and create or update app instances from that stack.

## Generate a one-service stack

If you also need a basic stack manifest for the generated service, scaffold both files:

```bash
wodby helm scaffold-stack \
  oci://registry-1.docker.io/bitnamicharts/memcached \
  --version 8.6.9 \
  --service-out service.yml \
  --stack-out stack.yml
```

Then validate both manifests:

```bash
wodby service validate-manifest service.yml --org 123
wodby stack validate-manifest stack.yml --org 123
```

Create the service first, then create the stack:

```bash
wodby service create-from-manifest service.yml --org 123 --version 8.6.9
wodby stack create-from-manifest stack.yml --org 123 --version 1.0.0
```

## When to edit manually

Expect to edit the scaffolded manifest when:

- the chart has more than one workload
- the chart renders CRDs, jobs, hooks, or cluster-scoped resources
- the chart needs persistent storage
- endpoint ports are not enough to describe how users should connect to the service
- users need configurable values exposed as Wodby settings
- the chart uses multiple container images with different tag policies
- the service needs links, tokens, volumes, backups, imports, configs, or actions

The scaffold is intentionally conservative. It gives you a valid baseline when the chart shape is simple, but a good
public service still needs a deliberate Wodby service model.

## CLI reference

- [`wodby helm inspect`](../cli/wodby_helm_inspect.html)
- [`wodby helm scaffold-service`](../cli/wodby_helm_scaffold-service.html)
- [`wodby helm scaffold-stack`](../cli/wodby_helm_scaffold-stack.html)
- [`wodby service validate-manifest`](../cli/wodby_service_validate-manifest.html)
- [`wodby service create-from-manifest`](../cli/wodby_service_create-from-manifest.html)
