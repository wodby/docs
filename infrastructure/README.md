# Infrastructure

When you [connect a server](../servers/README.md) to Wodby we deploy [container-based](../stacks/containers/README.md) infrastructure to this server. This will further allow you to deploy environment [for your applications](../apps/deploy.md) which we call [stacks](../stacks/README.md). 

Both server infrastructure and stacks have versioning. We regularly update them by releasing [newer versions](versioning.md), such updates can include security updates and performance improvements.
 
> The infrastructure we provide is based on [containers](../stacks/containers/README.md) and powered by Docker and Kubernetes.

## Cluster Schema

* [AWS](../cluster/aws.md)
* GCP (TBA) 
* Azure (TBA)
* Custom Data Center (TBA)

## Single-server Schema

![](_images/single-server-setup-schema.png)

Basic concepts:

* [Stacks](../stacks/README.md)
* [Containers](../stacks/containers/README.md)
* [Infrastructure versioning](versioning.md)

Further reading:

* [Adding SSH Key](keys.md)
* [Configuring UFW](ufw.md)
* [Monitoring](monitoring.md)
* [HTTP Strict Transport Security (HSTS)](hsts.md)
* [Using External Volumes](../volumes.md)
* [Environment Variables](../environment-variables.md)
* [Using Private Docker Registry](../docker-registry.md)
