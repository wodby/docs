# Single-server infrastructure

## Overview

When you connect a server to Wodby we deploy container-based infrastructure to this server. This will further allow you to your applications based on stacks.

!!! info "Wodby is not hosting provider"
    Wodby is not a hosting provider. We believe that there are plenty of reliable providers on the market already. You can connect your own servers from any hosting provider. By connecting your server, you let Wodby install infrastructure that will be used to deploy your apps.

Both server infrastructure and stacks have versioning. We regularly update them by releasing newer versions, such updates can include security updates and performance improvements.

* [Infrastructure maintenance](maintenance.md)
* [Stacks maintenance](../stacks/maintenance.md)

The infrastructure we provide is based strictly on containers and powered by Docker and Kubernetes.

## Schema

Edge is a reverse proxy container (nginx) that proxies requests to instances, perform redirects (http > https, www > non-www) and terminates SSL 

![](../assets/schema.png)​
