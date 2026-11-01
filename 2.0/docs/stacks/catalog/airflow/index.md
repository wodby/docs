# Apache Airflow

The Wodby Apache Airflow catalog stack runs Apache Airflow with a PostgreSQL service for its metadata. The current
composition and defaults are in [`wodby/stack-airflow`](https://github.com/wodby/stack-airflow).

## What the stack runs

Both services are required. One Airflow app service runs four containers on the same volume: the API server and web
interface (port 8080), the scheduler, the DAG processor, and the triggerer. Tasks run inside the scheduler container
(`LocalExecutor`). The service is not scalable.

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

## DAGs and plugins

The **Airflow data, DAGs, and logs** volume is mounted at `/opt/airflow` in every container. The stack creates it with
a size of 10 GB. Put DAG files in `/opt/airflow/dags` and plugins in `/opt/airflow/plugins`. The service has no build, so
DAGs are files on the volume and not part of an image. Wodby defines no backups or imports for this service.

## Change configuration

Add or change `AIRFLOW__*` [environment variables](../../../apps/environment-variables.md) on the Airflow app service
and deploy it. The scheduler, DAG processor, and triggerer are separate containers with their own variables. After a
change, check that it reached the container that uses it.

## Check that Airflow is healthy

`/api/v2/monitor/health` on port 8080 reports the state of the metadata database, scheduler, DAG processor, and
triggerer.
