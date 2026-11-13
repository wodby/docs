---
description: Deploy Apache Airflow with your DAGs, plugins and Python packages from Git on Wodby with the buildable Airflow stack, where every Airflow component runs your build.
---

# Apache Airflow (buildable)

The buildable Airflow stack runs [Apache Airflow](https://airflow.apache.org/) built from your Git repository: the
repository holds your DAGs, plugins and the Python packages they need, and every Airflow component runs the build. The
stack has the same services as the [Airflow stack](../airflow/index.md): Airflow and PostgreSQL. Its composition is
documented in [`wodby/stack-airflow-buildable`](https://github.com/wodby/stack-airflow-buildable).

Everything in the [Airflow guide](../airflow/index.md) applies, from the administrator account to the database. This
page covers what differs.

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

The API server, scheduler, DAG processor, triggerer and the setup step all run the build, so every component has your
code and packages. Changes reach Airflow with the next deployment.

## DAGs

Airflow reads DAGs and plugins from the build, not from the `dags` and `plugins` directories on the data volume. Keep
them in the repository.

To manage DAGs on Airflow's data volume yourself, use the [Airflow stack](../airflow/index.md).
