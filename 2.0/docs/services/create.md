# Create a service

A service is a reusable definition of software or behavior that can be added to a [stack](../stacks/index.md). Creating
a service makes it available to your organization or project, but it does not deploy anything by itself. To deploy it,
add the service to a stack, publish the stack, and create or upgrade an app instance from that stack.

For the stack step, see [Create a stack](../stacks/create.md).

## Choose a creation method

Use the method that matches how you want to own and update the service:

| Method | Use when |
| --- | --- |
| Dashboard from Git | You maintain `service.yml` in a Git repository and want Wodby to track that repository. |
| CLI Git import | You want the same Git-backed service import from automation or scripts. |
| Dashboard manifest creation | You have a local `service.yml` and want to create a non-Git-backed service. |
| CLI manifest creation | You want the same non-Git-backed service creation from automation or scripts. |
| Helm chart scaffold | You want to generate a starting `service.yml` from an existing Helm chart. |

## Start from Wodby repositories

Use Wodby's public repositories as working examples before writing a service from scratch:

- [`wodby/service`](https://github.com/wodby/service) is the boilerplate for a Git-backed service. It includes a small
  `service.yml`, starter `Dockerfile`, starter `.dockerignore`, and README guidance.
- [`wodby/services`](https://github.com/wodby/services) is the index of Wodby-managed services. It links to the source
  repository for each public service.

The boilerplate service defines a buildable HTTP service using the Wodby nginx Helm chart. Replace its example metadata,
options, image, Helm chart, settings, and build files with the service you want to publish. Keep workload and container
names stable after users create app services from the service, because stack and app-level overrides can depend on those
names.

For existing Wodby-managed service implementations, use the current
[`wodby/services`](https://github.com/wodby/services) index instead of copying repository links into this page.

## Wodby Helm charts

[`wodby/charts`](https://github.com/wodby/charts) contains Helm charts used by Wodby services. These charts are designed
for deployment through Wodby services and may not be generic standalone charts. Wodby handles some platform concerns,
such as certificates, selected config maps, and network policies, outside the chart manifests.

Use a chart from this repository when the service should deploy with a Wodby-maintained chart. Use the boilerplate
charts when you need a simple chart shape for a new service:

| Chart | Use when |
| --- | --- |
| [`stateless`](https://github.com/wodby/charts/tree/main/stateless) | The service runs stateless workloads such as HTTP applications, workers, or edge components. |
| [`stateful`](https://github.com/wodby/charts/tree/main/stateful) | The service needs stateful workload defaults such as a headless service or persistent storage support. |

Reference the selected chart in the `helm` section of `service.yml`, then expose any user-controlled chart values
through service settings, Helm values, or stack/app-level overrides.

## Create a Git-backed service

Use Git when you want the service manifest to remain the source of truth.

The repository must contain a `service.yml`, or an `index.yml` that lists multiple service directories:

```yaml
services:
  - php
  - nginx
```

Each listed directory must contain its own `service.yml`. See the [service template reference](template.md).

### Dashboard

1. Connect a Git provider integration if the repository is not already available. See [Git provider](../providers/git.md).
2. Open `Services`.
3. Select `New service from Git`.
4. Select the organization or project, Git integration, repository, ref type, and ref.
5. Create the service.

Git-backed services can later be updated from the same repository manually or automatically. See
[Service updates](updates.md).

### CLI

Use `wodby service import` for a Git-backed service:

```bash
wodby service import \
  --org 123 \
  --integration github-main \
  --remote-git-repo acme/custom-services \
  --git-ref main \
  --git-ref-type branch \
  --wait
```

To create the service in a project scope, include `--project`:

```bash
wodby service import \
  --org 123 \
  --project 456 \
  --integration github-main \
  --remote-git-repo acme/custom-services \
  --git-ref v1.0.0 \
  --git-ref-type tag \
  --wait
```

See [`wodby service import`](../cli/wodby_service_import.html) for all flags.

## Create from a local manifest

Use manifest creation when you have a `service.yml` file and do not need Wodby to track a Git repository.

### Dashboard

1. Open `Services`.
2. Select `New service from manifest`.
3. Select the organization or project that should own the service.
4. Paste the manifest YAML, or read it from a local `service.yml` file.
5. Enter the service version.
6. If the manifest references local files such as configs or Dockerfiles, add them under `Additional files` with the
   same paths used by the manifest.
7. Create the service.

### CLI

Validate the manifest first:

```bash
wodby service validate-manifest service.yml --org 123
```

Create the service:

```bash
wodby service create-from-manifest service.yml --org 123 --version 1.0.0
```

Create it in a project scope:

```bash
wodby service create-from-manifest service.yml --org 123 --project 456 --version 1.0.0
```

Use `--include` for referenced files such as configs or Dockerfiles when the manifest points to local files:

```bash
wodby service create-from-manifest service.yml \
  --org 123 \
  --version 1.0.0 \
  --include configs/app.conf \
  --include Dockerfile
```

See:

- [`wodby service validate-manifest`](../cli/wodby_service_validate-manifest.html)
- [`wodby service create-from-manifest`](../cli/wodby_service_create-from-manifest.html)

## Create from a Helm chart

Use the Helm scaffold workflow when an existing Helm chart mostly describes one logical service, such as Memcached,
Redis, a web server, or a single application workload. The Wodby CLI renders the chart, detects workloads and Kubernetes
Services, and generates a `service.yml` that you review before creating the service.

If the chart installs several independent application components, CRDs, operators, or cluster-scoped infrastructure,
review whether it should become a [stack](../stacks/index.md) or an [`infrastructure` service](types.md#infrastructure)
instead.

Start by inspecting the chart:

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

Check the generated fields before creating the service:

- `name`: stable machine name for the Wodby service.
- `type`: service type. Change it when the chart is a datastore, database, storage, or infrastructure service.
- `options[].version`: Wodby service option shown to users.
- `options[].tag`: container image tag appended to `workloads[].containers[].image`.
- `helm.source`, `helm.chart`, `helm.version`: chart reference Wodby uses for validation and deployment.
- `workloads[].selector.matchLabels`: must match exactly one rendered Kubernetes workload.
- `endpoints[]`: ports Wodby exposes for stack and app-service configuration.

After reviewing the generated `service.yml`, validate and create it with the same manifest workflow used for any custom
service:

```bash
wodby service validate-manifest service.yml --org 123
wodby service create-from-manifest service.yml --org 123 --version 1.0.0
```

Expect to edit the scaffolded manifest when:

- the chart has more than one workload
- the chart renders CRDs, jobs, hooks, or cluster-scoped resources
- the chart needs persistent storage
- endpoint ports are not enough to describe how users should connect to the service
- users need configurable values exposed as Wodby settings
- the chart uses multiple container images with different tag policies
- the service needs links, tokens, volumes, backups, imports, configs, or actions

The scaffold is intentionally conservative. It gives you a valid baseline when the chart shape is simple, but a good
public service still needs a deliberate Wodby service model. For full manifest details, see the
[service template reference](template.md).

See:

- [`wodby helm inspect`](../cli/wodby_helm_inspect.html)
- [`wodby helm scaffold-service`](../cli/wodby_helm_scaffold-service.html)

## After creating the service

A service must be referenced by a stack before it can be deployed by an app.

1. Create or update a stack that includes the service. See [Create a stack](../stacks/create.md).
2. Configure stack-service defaults such as options, env vars, volumes, links, settings, and Helm values.
3. Publish the stack revision when needed.
4. Create an app or app instance from the stack.

For ongoing service revisions and stack behavior, see [Service updates](updates.md) and [Stack updates](../stacks/updates.md).
