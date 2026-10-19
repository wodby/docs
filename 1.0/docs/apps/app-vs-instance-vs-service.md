# App vs Instance vs Service

An app groups the deployed copies of your application. Each copy is an instance, and each instance runs the services defined by its stack.

## Quick model

| Object | What it represents | Example | Where you work with it |
| --- | --- | --- | --- |
| App | The application that groups related instances | `shop` | Apps |
| Instance | One isolated environment of the application | `dev`, `staging`, `production` | Instances and the selected instance's pages |
| Service | One part of an instance's stack | PHP, Nginx, MariaDB, Redis | Instance > Stack |

For example, the `shop` app can have development and production instances. Each instance has its own configured services. The two instances can run on different connected servers.

## App

An app groups instances of the same application. Every app has at least one instance; you choose the stack and configure the first instance when [creating an app](new.md).

Use the app's **Instances** page to add, remove, or select an instance. Deleting the last instance also deletes the app. See [instance deletion](instances.md#deleting-an-instance) for the effects on resources and retained data.

## Instance

An instance is one isolated environment of an app. In Wodby 1, this is the deployed copy you work with when changing domains, deploying code, or managing backups.

Each instance has its own:

- destination server;
- instance type and stack configuration;
- services and their configuration;
- domains and published ports;
- code deployment settings and CI builds; and
- database and persistent files, with backup operations provided by its stack.

The default instance types are **dev**, **staging**, and **production**. A type influences stack behavior, such as error reporting and health checks. The exact differences depend on the stack. See [Instance type](instances.md#instance-type).

Instances can be configured and upgraded separately. Updating the stack in your organization makes an update available; upgrading an instance applies it to that instance. See [Stacks maintenance](../stacks/maintenance.md).

## Service

A stack defines the services needed by an application. A service has one or more available container implementations, such as Nginx or Apache for an HTTP server. Some services are required; others, such as a cache, may be optional.

Open **Instance > Stack** to configure a service. Depending on the stack, you can change its implementation, environment variables, replicas, resource limits, and public ports, or enable and disable optional services. Redeploy the stack to apply configuration changes.

The service describes a part of the application; its containers run that software on the connected server. See [Stack configuration](../stacks/config.md) and [Accessing containers](../infrastructure/containers.md#accessing-containers).

## Choose the right level

- Work with the **app** to organize its instances.
- Select an **instance** to deploy code, attach a domain, or create a backup for one environment.
- Configure a **service** to change how one component runs in that instance.

## Related pages

- [Create an app](new.md)
- [Instances](instances.md)
- [Stacks](../stacks/index.md)
- [Glossary](../glossary.md)
