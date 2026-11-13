---
description: Run your own Dagster assets, jobs and schedules on Wodby with the buildable Dagster stack, which builds your Dagster project as a code location that Dagster loads.
---

# Dagster (buildable)

The buildable Dagster stack runs [Dagster](https://dagster.io/) with your own code: your Git repository holds a Dagster
project, and Wodby builds it as a code location that Dagster's webserver and daemon load. The stack runs the Dagster
webserver and daemon, the code location and a PostgreSQL database. Its composition is documented in
[`wodby/stack-dagster-buildable`](https://github.com/wodby/stack-dagster-buildable).

Everything in the [Dagster guide](../dagster/index.md) applies, from opening the Dagster interface to the database.
This page covers what differs.

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

## Code location and runs

The stack sets Dagster's workspace to load the `app` code location from the `code` service. Every deployment builds a
new image and restarts the code server, and Dagster reloads the code location.

Runs execute inside the code server, which has your code and packages, and their events are stored in PostgreSQL. Give
the code service enough memory and CPU for your runs. Outputs that Dagster's default IO manager writes to the code
server's disk don't survive a restart: configure an IO manager that writes to external storage for outputs that later
runs read.

To run Dagster with code locations that run elsewhere, use the [Dagster stack](../dagster/index.md).
