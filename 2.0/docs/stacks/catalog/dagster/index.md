---
description: Run your own Dagster assets, jobs and schedules on Wodby with the Dagster stack, which builds your Dagster project from Git as a code location that Dagster loads.
---

# Dagster

The Wodby Dagster stack runs [Dagster](https://dagster.io/) with your own code: your Git repository holds a Dagster
project, and Wodby builds it as a code location that Dagster's webserver and daemon load. The stack runs the Dagster
webserver and daemon, the code location and a PostgreSQL database, and all three are required. Its composition is
documented in [`wodby/stack-dagster`](https://github.com/wodby/stack-dagster).

## Repository

Start the repository from the [Dagster boilerplate](https://github.com/wodby/dagster-boilerplate) and connect it to the
`code` service when you create the app.

| Path | Purpose |
| --- | --- |
| `app/definitions.py` | The code location's `Definitions`: your assets, jobs, schedules and sensors |
| `requirements.txt` | Python packages your code needs |

The code server loads the `app.definitions` module. To load another module, change the code service's **Python
module** setting.

## Build

The build starts from the Dagster image of the Dagster service's version, so the code location runs the same Dagster
as the webserver and daemon. It installs `requirements.txt` and fails when the packages change Dagster's version:
don't list `dagster` itself, and use Dagster libraries that match its version.

## Open the Dagster interface

Wodby protects the Dagster app service's public domains with HTTP basic authentication. Find the generated password in
**Apps > [App] > [Environment] > Endpoints > Auths**. Other services in the same app environment reach Dagster without
the password. You can turn the protection off when you create the app, or later by deleting the entry. See
[Auths](../../../apps/endpoints.md#auths).

## Code locations

The stack sets the Dagster service's **Workspace** config (`workspace.yaml`) to load the `app` code location from the
`code` service. Every deployment builds a new image and restarts the code server, and Dagster reloads the code
location.

To load more code locations, such as gRPC servers that run elsewhere, open the Dagster app service's
**Configuration > Configs** tab, override the **Workspace** config, add them next to `app`, and deploy the app service.

## Runs

Runs execute inside the code server, which has your code and packages, and their events are stored in PostgreSQL. Give
the code service enough memory and CPU for your runs. Outputs that Dagster's default IO manager writes to the code
server's disk don't survive a restart: configure an IO manager that writes to external storage for outputs that later
runs read.

The **Wipe all run history** action deletes all run history and event logs. It cannot be undone.

## Data and backups

Dagster has no volume. Runs, events, and schedules are stored in the linked PostgreSQL database, so back up that
database. See [Backups](../../../apps/backups.md) and [Database details](../../../databases/index.md).

## Limits

The Dagster and code location services are not scalable.
