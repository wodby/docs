---
description: Rules for machine names in Wodby, including Kubernetes names, environment namespaces, service names, port names, generated resource names and database names.
---

# Naming rules

Machine names are permanent identifiers used in URLs, generated Kubernetes resources, stack and service templates, and provider APIs. Prefer short, descriptive names.

## General Kubernetes names

Use this rule for app names, app environment names, stack names, top-level service names in `service.yml`, workload names, container names, endpoint names, volume names, config names, and workload references.

Names must:

- contain only lowercase letters `a-z`, numbers `0-9`, and dashes `-`
- start and end with a lowercase letter or number
- be 63 characters or shorter

### App environment namespaces

Each app environment runs in its own Kubernetes namespace, generated as:

```text
<app-name>-<environment-name>
```

The generated namespace must:

- be 63 characters or shorter, so keep app and environment names short enough for the combined value
- be unique in its cluster. Two different pairs of names can produce the same namespace: app `shop-eu` with environment `prod` and app `shop` with environment `eu-prod` both produce `shop-eu-prod`
- not be a reserved namespace: `default`, any name starting with `kube-`, or a namespace of a Wodby cluster component (`envoy-gateway`, `frpc`, `ingress-nginx`, `monitoring`, `wsp-client`)

Wodby checks these rules when you create an app or an environment and when you [move an environment to another cluster](apps/migration.md). If the namespace is reserved or already used in the cluster, choose a different app or environment name.

Wodby deploys an environment only into a namespace it created for that environment. If the cluster already has a namespace with the generated name that was created outside Wodby, the deployment stops with an error and that namespace is left unchanged. Remove the namespace from the cluster, or use a different app or environment name. Deleting the environment also leaves such a namespace in place.

Some dashboard route words are reserved, such as `new`, `settings`, and `clusters`, even if they otherwise match the character rules.

## Kubernetes service names

Use this rule for stack service names, stack derivative names, app service names, and derivative service names.

Names must:

- contain only lowercase letters `a-z`, numbers `0-9`, and dashes `-`
- start with a lowercase letter
- end with a lowercase letter or number
- be 63 characters or shorter

Because derivative service names include the parent service name as a prefix, services that define or inherit derivatives should use service names that start with a letter.

## Port names

Service endpoint port names must:

- contain only lowercase letters `a-z`, numbers `0-9`, and dashes `-`
- start and end with a lowercase letter or number
- include at least one letter
- not contain consecutive dashes
- be 15 characters or shorter

## Generated resource names

Wodby builds some Kubernetes names from your names, and these must also fit Kubernetes length limits. Wodby checks them before app services are created or deployed.

If deployment fails because a generated name is too long, shorten the app, environment, stack service, storage service, volume, or config name that contributes to it.

## Database names

For app-created container databases, Wodby generates database names from the app, environment, and service names.

For managed provider databases, the provider-facing database name must use lowercase letters, numbers, and dashes, start with a letter, end with a letter or number, and be 3 to 32 characters long.
