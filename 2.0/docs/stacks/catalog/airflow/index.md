---
description: Deploy Apache Airflow with your DAGs, plugins and Python packages from Git on Wodby with the Apache Airflow stack, where every Airflow component runs your build and PostgreSQL holds the metadata.
---

# Apache Airflow

The Wodby Apache Airflow stack runs [Apache Airflow](https://airflow.apache.org/) built from your Git repository: the
repository holds your DAGs, plugins and the Python packages they need, and every Airflow component runs the build.
PostgreSQL holds Airflow's metadata. The current composition and defaults are in
[`wodby/stack-airflow`](https://github.com/wodby/stack-airflow).

## Repository

Start the repository from the [Airflow boilerplate](https://github.com/wodby/airflow-boilerplate) and connect it when
you create the app.

| Path | Purpose |
| --- | --- |
| `dags/` | Your DAGs |
| `plugins/` | Your Airflow plugins |
| `requirements.txt` | Python packages your DAGs need, such as providers |

## Build

Choose the Airflow version when you create the app. The build starts from the official Airflow image of that version,
adds your DAGs and plugins, and installs `requirements.txt` with Airflow pinned to that version: a package that needs
another Airflow version fails the build. Don't list `apache-airflow` itself.

Changes to DAGs, plugins or packages reach Airflow with the next deployment. Airflow reads DAGs and plugins from the
build, not from the `dags` and `plugins` directories on the data volume, so keep them in the repository.

## What the stack runs

Both services are required. One Airflow app service runs four containers on the same volume: the API server and web
interface (port 8080), the scheduler, the DAG processor, and the triggerer. All four, and the setup step that runs
before them, use the build. Tasks run inside the scheduler container (`LocalExecutor`). The service is not scalable.

PostgreSQL is Airflow's metadata database. Wodby sets the connection in `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`, so do not
set it elsewhere. The stack creates a 20 GB PostgreSQL volume. See [Databases](../../../databases/index.md).

## Sign in

Open the Airflow domain listed under **Endpoints** for the app environment. Before the containers start, Wodby
migrates the metadata database and creates an administrator account. Open the Airflow app service's
**Configuration > Tokens** tab and reveal `admin_username` (`admin`) and `admin_password`. If the user already exists,
Wodby leaves it as it is. See [Tokens](../../../apps/tokens.md).

The stack also generates `fernet_key`, `api_secret_key`, and `api_auth_jwt_secret`. Airflow uses the Fernet key to
encrypt connection passwords stored in the database. The other two secure API server sessions and tokens between
Airflow components.

Users are managed by Airflow's FAB auth manager. Example DAGs are off.

## Data volume

The **Airflow data, DAGs, and logs** volume is mounted at `/opt/airflow` in every container and holds Airflow's logs.
The stack creates it with a size of 10 GB. Wodby defines no backups or imports for this service; your code lives in
Git and the metadata in PostgreSQL.

## Change configuration

Add or change `AIRFLOW__*` [environment variables](../../../apps/environment-variables.md) on the Airflow app service
and deploy it. The scheduler, DAG processor, and triggerer are separate containers with their own variables. After a
change, check that it reached the container that uses it.

## Check that Airflow is healthy

`/api/v2/monitor/health` on port 8080 reports the state of the metadata database, scheduler, DAG processor, and
triggerer.
