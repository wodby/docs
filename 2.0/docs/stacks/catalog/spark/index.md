---
description: Run an Apache Spark standalone cluster on Wodby with the Apache Spark catalog stack, with a Spark master and worker services linked for you.
---

# Apache Spark

The Wodby Apache Spark catalog stack runs a Spark standalone cluster with a Spark master and Spark worker services.
The current composition and defaults are in [`wodby/stack-spark`](https://github.com/wodby/stack-spark).

## What the stack runs

Both services are required. The worker is linked to the master, and Wodby sets the master address on the worker for
you, so do not set it elsewhere. The stack starts with one worker.

## Connect an application

Applications reach the master at `spark://<master app service name>:7077`. This port is private: other
services in the same app environment can reach it, and Wodby creates no public route for it.

## Open the master web interface

The master web interface is on port 8080 and is protected with basic auth by default. Each app service gets its own
generated password. Reveal it under **Endpoints > Auths** for the app environment. See
[Auths](../../../apps/endpoints.md#auths). Services inside the environment reach the master directly, without the
password.

## Add workers and size them

The worker service is scalable: each replica is one worker. Set the replica count as described in
[Application Scalability](../../../apps/scalability.md).

Each worker offers CPU and memory to the master through these settings on the worker app service:

| Setting | Default | Meaning |
| --- | --- | --- |
| **Worker CPU cores** | `2` | Cores that Spark applications may use on this worker |
| **Worker memory** | `2g` | Memory that Spark applications may use on this worker |

These settings are separate from the container's CPU and memory resources. Keep them within the container's limits.

## Limits

- The master is not scalable and has no volume.
- Workers have no volume. Application work directories are lost when a worker pod is replaced.
- The worker web interface (port 8081) is not reachable from other services.
- Other Spark settings are environment variables on the app service. The master's ports and listen address are fixed.
  See [environment variables](../../../apps/environment-variables.md).
