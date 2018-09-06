# PostgreSQL stack documentation

PostgreSQL can be configured with the following [environment variables](https://github.com/wodby/postgres#environment-variables)

## Local environment

if you want to import your database, uncomment the line for `postgres-init` volume in your compose file. Create the volume directory `./postgres-init` in the same directory as the compose file and put there your `.sql .sql.gz .sh` file(s). All SQL files will be automatically imported once Postgres container has started.

## Changelog

This changelog is for PostgreSQL stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/postgres/releases).

### 1.2.2

PostgreSQL patch updates: 10.5, 9.6.10, 9.5.14, 9.4.19, 9.3.24

### 1.2.1

PostgreSQL patch updates: 10.4, 9.6.9, 9.5.13, 9.4.18, 9.3.23

### 1.2.0

* PostgreSQL updated to 10.2, 9.6.7, 9.5.11, 9.4.16, 9.3.21
* Default [memory request](../config.md#resources) set to 64m

### 1.1.0

* New PostgreSQL 10.1
* PostgreSQL versions updated and freezed: 9.6.6, 9.5.10, 9.4.15, 9.3.20
* PostgreSQL 9.2 has reached end of life and dropped
* Shutdown grace period increased to 5 minutes
* Health check timeout increased to 30 seconds
* Backup action now runs with `nice` (10) and `ionice` (7)
* Improved error handling in import action

### 1.0.1

* Versions freeze: 9.6.3, 9.5.7, 9.4.12, 9.3.17, 9.2.21
* Add new environment variable `POSTGRES_DB_EXTENSIONS` to create extensions

### 1.0.0

Initial release
