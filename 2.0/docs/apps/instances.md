# Instances

![](./images/instance.svg)

Application instance is a single isolated copy of your application that deployed to a [kubernetes cluster](../kubernetes/index.md) and has:

- [Environment](env.md) (like production, staging)
- [Stack](stack.md) with a specific revision 
- [Endpoints](endpoints) to configure domains and public ports
- [Builds](builds.md) (if stack contains buildable services) and [deploys](deploys.md)
- [Backups](backups.md) and [imports](imports.md) (if stack contains services that provide such)
- [App Services](services.md) per each service that used to override stack configuration for this specific instance
- Live [logs streaming](logs.md) 
- [Cron](cron.md) schedules and jobs 
- [Tasks](tasks.md) history

You can remove or add a new instance from the _"[App] > Instances"_ page.
