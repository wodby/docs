Source: https://wodby.com/docs/2.0/providers/databases/

# Database providers

Database providers are third-party services whose integrations expose the `db` type. Use this group when you want Wodby to create and manage provider-managed database servers inside your cloud account.

Machine name: `db`

Use a database provider when:

- you want Wodby to provision a managed database in your cloud account
- you want database lifecycle operations to stay tied to the provider integration
- you need a cloud-managed MySQL, MariaDB, or PostgreSQL server instead of an app-level database service

## Where it is used in Wodby

Database integrations are used for:

- creating managed databases
- selecting the cloud account used for managed database provisioning
- reusing the same provider connection across multiple managed database resources

## Supported providers

| Provider | Managed service |
| --- | --- |
| [Amazon Web Services](https://wodby.com/docs/2.0/providers/aws/#rds) | RDS |
| [Azure](https://wodby.com/docs/2.0/providers/azure/#databases) | Azure managed databases |
| [Google Cloud Platform](https://wodby.com/docs/2.0/providers/gcp/#cloud-sql) | Cloud SQL |
| [DigitalOcean](https://wodby.com/docs/2.0/providers/digitalocean/#managed-database) | Managed Database |

- Use an app-level database service when the database should live inside the application stack.
- Use an external database connection only when the database already exists outside Wodby and does not need to be provisioned by Wodby.

## Related pages

- [Integration types](https://wodby.com/docs/2.0/integrations/types/)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
- [Managed databases](https://wodby.com/docs/2.0/databases/managed/)
- [Database services](https://wodby.com/docs/2.0/services/types/#db)
