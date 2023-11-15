# Integrations

Wodby provides native integration with third-party services through _providers_. _Integration_ represents a single connection between your Wodby account with your third-party service account. For example, you create a new integration of the AWS provider to connect your AWS account to Wodby to e.g. create a new EKS cluster.

## Provider

Apart from [variable](variable.md) type providers, all providers offered and maintained by Wodby. If you think there's a good provider that we should add to Wodby, please let us know. 

## Types

Every provider can have multiple integration types it offers. When you create a new integration you can select which type you want to create. Supported integration types listed below:

### Kubernetes

- [Google Cloud Platform GKE](gcp.md#gke)
- [Amazon Web Services EKS](aws.md#eks)
- [Azure AKS](azure.md#aks)
- [DigitalOcean DOKS](digitalocean.md#doks)
- [OVH Kubernetes](ovh.md#kubernetes)
- [Linode](linode.md#lke)

### Databases

- [Google Cloud Platform Cloud SQL](gcp.md#cloud-sql)
- [Amazon Web Services RDS](aws.md#rds)
- [Azure Databases](azure.md#databases)
- [DigitalOcean Managed Database](digitalocean.md#managed-database)

### Storage

- [Amazon Web Services S3](aws.md#s3)
- [Google Cloud Platform Cloud Storage](gcp.md#cloud-storage)
- [Azure Blob Storage](azure.md#blob-storage)
- [DigitalOcean Spaces](digitalocean.md#spaces)

### CI/CD

- [Wodby CI](../cicd/wodby-ci.md)
- [CircleCI](circleci.md)
- [GitHub Actions](github.md#actions)

### Docker registry

- [Wodby Registry](../cicd/wodby-registry.md)
- [Docker Hub](docker.md)

### Monitoring

- [NewRelic](newrelic.md)
- [Datadog](datadog.md)

### Variable

- [NewRelic](newrelic.md)
- [Sentry](sentry.md)
