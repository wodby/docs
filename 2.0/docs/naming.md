# Naming rules

Machine names are permanent identifiers used in URLs, generated Kubernetes resources, stack and service templates, and provider APIs. Prefer short, descriptive names.

## General Kubernetes names

Use this rule for app names, app instance names, stack names, top-level service names in `service.yml`, workload names, container names, endpoint names, volume names, config names, and workload references.

Names must:

- contain only lowercase letters `a-z`, numbers `0-9`, and dashes `-`
- start and end with a lowercase letter or number
- be 63 characters or shorter

App instance Kubernetes namespaces are generated as:

```text
<app-name>-<instance-name>
```

The generated namespace must also be 63 characters or shorter, so keep app and instance names short enough for the combined value.

Some dashboard route words are reserved, such as `new`, `settings`, and `clusters`, even if they otherwise match the character rules.

## Kubernetes service names

Use this rule for stack service names, stack derivative names, app service names, and derivative service names.

Names must:

- contain only lowercase letters `a-z`, numbers `0-9`, and dashes `-`
- start with a lowercase letter
- end with a lowercase letter or number
- be 63 characters or shorter

These names become Kubernetes service-facing identifiers, so they are stricter than the general Kubernetes name rule.

Because derivative service names include the parent service name as a prefix, services that define or inherit derivatives should use service names that start with a letter.

## Port names

Service endpoint port names must:

- contain only lowercase letters `a-z`, numbers `0-9`, and dashes `-`
- start and end with a lowercase letter or number
- include at least one letter
- not contain consecutive dashes
- be 15 characters or shorter

## Generated resource names

Wodby validates generated Kubernetes names before app services are created or deployed. This includes namespaces, app service names, generated PVC names, generated ConfigMap names, storage class names for shared storage, and additional Kubernetes manifests.

If deployment fails because a generated name is too long, shorten the app, instance, stack service, storage service, volume, or config name that contributes to it.

## Database names

For app-created container databases, Wodby generates internal database entity names from the app, instance, and service names.

For managed provider databases, the provider-facing database name must use lowercase letters, numbers, and dashes, start with a letter, end with a letter or number, and be 3 to 32 characters long.
