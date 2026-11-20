Source: https://wodby.com/docs/2.0/integrations/types/

# Integration types

Every provider can expose one or more integration types. When you create an integration, the selected type determines where that integration can be used in Wodby.

Use the directory below to jump to the type you need. Type-specific overview pages live in the [Providers](https://wodby.com/docs/2.0/providers/) section because that is where providers are grouped in the navigation.

| Type | Machine name | Typical use | Provider group |
| --- | --- | --- | --- |
| Kubernetes | `kubernetes` | Create managed Kubernetes clusters in supported cloud accounts | [Kubernetes providers](https://wodby.com/docs/2.0/providers/kubernetes/) |
| Databases | `db` | Create managed databases in supported cloud accounts | [Database providers](https://wodby.com/docs/2.0/providers/databases/) |
| Storage | `storage` | Store app and database backups in object storage | [Storage providers](https://wodby.com/docs/2.0/providers/storage/) |
| Git | `git` | Connect repositories for remote build sources | [Git providers](https://wodby.com/docs/2.0/providers/git/) |
| CI | `ci` | Run builds and deployments from Wodby CI or third-party CI | [CI providers](https://wodby.com/docs/2.0/providers/ci/) |
| Registry | `registry` | Push and pull build images from container registries | [Registry providers](https://wodby.com/docs/2.0/providers/registry/) |
| SMTP | `smtp` | Relay outbound email through a provider | [SMTP providers](https://wodby.com/docs/2.0/providers/smtp/) |
| Private App Access | `application_access` | Route an app or selected HTTP endpoints through an access provider | [Private App Access providers](https://wodby.com/docs/2.0/providers/access/) |
| VPN | `vpn` | Deploy a persistent service-managed node on a private network | [VPN providers](https://wodby.com/docs/2.0/providers/vpn/) |
| Variable | `variable` | Reuse provider-backed environment variables across apps and stacks | [Variable integrations](https://wodby.com/docs/2.0/integrations/variable/) |

## Notes

- Some providers support more than one type. For example, AWS can be used for Kubernetes, databases, storage, SMTP,
  and variables, Cloudflare supports Private App Access and variables, and Tailscale supports Private App Access and
  service-managed VPN nodes.
- Type pages explain the type-level workflow. Provider pages explain the exact fields, auth methods, and exposed environment variables.

## Related pages

- [Integrations overview](https://wodby.com/docs/2.0/integrations/)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
- [Provider vs integration](https://wodby.com/docs/2.0/integrations/providers-vs-integrations/)
