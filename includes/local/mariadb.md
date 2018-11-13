#### Import existing database

!!! danger "Known issues with indexes rebuild"
    Issues have been reported when MariaDB does not build indexes when dump imported using `mariadb-init` bind mount. For safety use the workaround described at https://github.com/wodby/mariadb/issues/11

if you want to import your database, uncomment the line for `mariadb-init` bind mount in your compose file. Create the directory `./mariadb-init` in the same directory as the compose file and put there your `.sql .sql.gz .sh` file(s). All SQL files will be automatically imported once MariaDB container has started.

#### Export

Exporting all databases:
```shell
docker-compose exec mariadb sh -c 'exec mysqldump --all-databases -uroot -p"root-password"' > databases.sql
```

Exporting a specific database:
```shell
docker-compose exec mariadb sh -c 'exec mysqldump -uroot -p"root-password" my-db' > my-db.sql
```
