# Service Kubernetes metadata

Some services need additional Kubernetes-specific metadata beyond their Helm settings. This is defined under the
[`kubernetes` section](template.md#kubernetes) in the service template.

This section is optional and only needed for services that must integrate with platform-level infrastructure.

## Infrastructure selectors

Currently, the `kubernetes` section supports `infrastructure` selectors.

Use `kubernetes.infrastructure` to describe which infrastructure services a service can work with. Each item includes:

- `name`: the machine name of the infrastructure dependency
- `title`: an optional human-readable label
- `selectors`: rules used to match compatible services

Selectors use the same structure as [service link selectors](links.md): `type`, optional `option`, and optional
`labels`.

```yaml
kubernetes:
  infrastructure:
    - name: monitoring
      title: Monitoring
      selectors:
        - type: infrastructure
          labels:
            - monitoring
```

Use this when a service depends on infrastructure provided elsewhere in the environment.
