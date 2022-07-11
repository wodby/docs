# PostgreSQL stack documentation

PostgreSQL can be configured with the following [environment variables](https://github.com/wodby/postgres#environment-variables)

## External access

There are two ways to connect to a PostgreSQL server externally: publish port or set up an SSH tunnel.

### Publish port

Publish PostgreSQL's port (5432) from [stack configuration page](../config.md#ports) to a dynamic node port and connect as:

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

### 1.6.1

⬆️ Postgres 14.4

### 1.6.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- 🏔 Alpine Linux updated to 3.15

### 1.5.1

🏔 Security updates for base OS Alpine Linux

### 1.5.0

- ⭐️ Added PostgreSQL 12, 13, 14
- 🪦 PostgreSQL 9.6 dropped (EOL)
- ⬆️ Updated to 11.15, 10.20

### 1.4.0

- ⬆️ PostgreSQL 11.14, 10.19, 9.6.24
- 🥶 Rebased to [wodby/base-postgres](https://github.com/wodby/base-postgres) with frozen Alpine 3.13

### 1.3.15

- ⬆️&nbsp; PostgreSQL 13.3, 12.7, 11.12, 10.17, 9.6.22
- ⬆️&nbsp; Adminer 4.8.1

### 1.3.14

📦&nbsp; Base OS Alpine Linux updated to 3.13.5

### 1.3.13

- ⬆️&nbsp; Updates: 13.2, 12.6, 11.11, 10.16, 9.6.21
- 🚨&nbsp; Versions 9.4, 9.5 have reached EOL

### 1.3.12

- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 1.3.11

PostgreSQL 12.5, 11.10, 10.15, 9.6.20, 9.5.24

### 1.3.10

PostgreSQL 12.4, 11.9, 10.14, 9.6.19, 9.5.23

### 1.3.9

- PostgreSQL 12.3, 11.8, 10.13, 9.6.18, 9.5.22
- Adminer 4.7.7

### 1.3.8

- PostgreSQL 12.2, 11.7, 10.12, 9.6.17, 9.5.21, 9.4.26
- Adminer 4.7.6

### 1.3.7

- PostgreSQL updates: 11.6, 10.11, 9.6.16, 9.5.20, 9.4.25
- Adminer 4.7.5

### 1.3.6

PostgreSQL updates: 11.5, 10.10, 9.6.15, 9.5.19, 9.4.24

### 1.3.5

- PostgreSQL updates: 11.4, 10.9, 9.6.14, 9.5.18, 9.4.23
- Adminer updated to 4.7.2
- Alpine Linux updated to 3.10.1

### 1.3.4

- PostgreSQL updates: 11.3, 10.8, 9.6.13, 9.5.17, 9.4.22
- Alpine Linux updated to 3.9.4

### 1.3.3

- Alpine Linux updated to 3.9.3
- Adminer rebuilt against latest base image

### 1.3.2

- PostgreSQL:
  - Version 9.3 has reached EOL and will no longer receive updates
  - Patch updates: 11.2, 10.7, 9.6.12, 9.5.16, 9.4.21
- Adminer updated to 4.7.1 and rebuilt against latest base image

### 1.3.1

* Adminer updated to 4.7.0 and rebuilt against latest base image

### 1.3.0

* PostgreSQL 11 added
* PostgreSQL patch updates: 10.6, 9.6.11, 9.5.15, 9.4.20, 9.3.25

### 1.2.4

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
