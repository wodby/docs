# PostgreSQL stack documentation

PostgreSQL can be configured with the following [environment variables](https://github.com/wodby/postgres#environment-variables)

## External access

There are two ways to connect to a PostgreSQL server externally: publish port or set up an SSH tunnel.

### Publish port

Publish PostgreSQL's port (5432) from [stack configuration page](../../stacks/config.md#ports) to a dynamic node port and connect as:

```shell
psql -h [IP] -p [PORT] -U [USER] -W [PASSWORD] [DATABASE]
```

Where `[PORT]` is the generated node port (you can find it on a service page `App Instance > Stack > PostgreSQL`) and `[IP]` is the IP of the server where your app instance deployed (or use the server hostname `node-[SERVER UUID].wod.by`).

### Set up tunnel

If you deploy PostgreSQL as a service inside of a stack that comes with an SSHD container, you can set up a secure tunnel:

1. Set up an SSH tunnel on port `55432` (you can change it). You can find `[SSH Port]` on `Instance > Stack > SSH` page. For PostgreSQL (port `5432` by default) use the following command:    
    ```shell
    ssh -L 55432:postgres:5432 -p [SSH Port] wodby@[Server IP] -N
    ```
2. Connect to the database via the tunnel on port `5432` (replace `[tokens]`):
    ```shell
    psql -p 55432 -U [USER] -W [PASSWORD] [DATABASE]
    ```

## Changelog

This changelog is for PostgreSQL stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/postgres/releases).

## 1.3.3

- Base OS Alpine Linux updated to 3.9.3
- Adminer rebuilt against latest base image

## 1.3.2

- PostgreSQL:
  - Version 9.3 has reached EOL and will no longer receive updates
  - Patch updates: 11.2, 10.7, 9.6.12, 9.5.16, 9.4.21
- Adminer updated to 4.7.1 and rebuilt against latest base image

## 1.3.1

* Adminer updated to 4.7.0 and rebuilt against latest base image

## 1.3.0

* PostgreSQL 11 added
* PostgreSQL patch updates: 10.6, 9.6.11, 9.5.15, 9.4.20, 9.3.25

## 1.2.4

* Adminer: 
    * Bugfix: some `$PHP_` env vars were ignored
    * Default memory limit set to 512M
    * Adminer and Webgrind rebuilt against latest base image

### 1.2.3

Adminer service added

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
