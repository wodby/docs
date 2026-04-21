# Integration types

Every provider can expose one or more integration types. When you create an integration, the selected type determines where that integration can be used in Wodby.

Use the directory below to jump to the type you need. Type-specific overview pages live in the [Providers](../providers/index.md) section because that is where providers are grouped in the navigation.

| Type | Machine name | Typical use | Provider group |
| --- | --- | --- | --- |
| Kubernetes | `kubernetes` | Create managed Kubernetes clusters in supported cloud accounts | [Kubernetes providers](../providers/kubernetes.md) |
| Databases | `db` | Create managed databases in supported cloud accounts | [Database providers](../providers/databases.md) |
| Storage | `storage` | Store app and database backups in object storage | [Storage providers](../providers/storage.md) |
| Git | `git` | Connect repositories for remote build sources | [Git providers](../providers/git.md) |
| CI | `ci` | Run builds and deployments from Wodby CI or third-party CI | [CI providers](../providers/ci.md) |
| Registry | `registry` | Push and pull build images from container registries | [Registry providers](../providers/registry.md) |
| SMTP | `smtp` | Relay outbound email through a provider | [SMTP providers](../providers/smtp.md) |
| VPN | `vpn` | Join supported services to a private network | [VPN providers](../providers/vpn.md) |
| Variable | `variable` | Reuse provider-backed environment variables across apps and stacks | [Variable integrations](variable.md) |

## Notes

- Some providers support more than one type. For example, AWS can be used for Kubernetes, databases, storage, SMTP, and variables.
- Type pages explain the type-level workflow. Provider pages explain the exact fields, auth methods, and exposed environment variables.

## Related pages

- [Integrations overview](index.md)
- [Providers overview](../providers/index.md)
- [Provider vs integration](providers-vs-integrations.md)
