# Infrastructure

When you [connect a server](../servers/README.md) to Wodby we deploy [container-based](../stacks/containers/README.md) infrastructure to this server. This will further allow you to deploy environment [for your applications](../apps/deploy.md) which we call [stacks](../stacks/README.md). 

Both server infrastructure and stacks have versioning. We regularly update them by releasing [newer versions](versioning.md), such updates can include security updates and performance improvements.
 
> The infrastructure we provide is based on [containers](../stacks/containers/README.md) and powered by Docker and Kubernetes.

Basic concepts:

* [Stacks](../stacks/README.md)
* [Containers](../stacks/containers/README.md)
* [Schema](schema.md)
* [Infrastructure versioning](versioning.md)

Further reading:

* [Adding SSH Key](keys.md)
* [CLI commands](cli.md)
* [Cloudflare integration](cloudflare.md)
* [Configuring UFW](ufw.md)
* [Cron](cron.md)
* [HTTP Strict Transport Security (HSTS)](hsts.md)
* [Infrastructure memory consumption](memory-consumption.md)
* [Integration with CloudFlare](cloudflare.md)
* [Local development](local.md)
* [Mail Transfer Agent (SMTP)](mta.md)
* [Security](security.md)
