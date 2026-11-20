Source: https://wodby.com/docs/2.0/stacks/catalog/postgis/

# PostGIS stack guide

The Wodby PostGIS catalog stack runs a PostgreSQL database server that bundles PostGIS. The current composition is
documented in [`wodby/stack-postgis`](https://github.com/wodby/stack-postgis). It has one service, with a 20 GB `data`
volume. It has no Adminer or pgAdmin option.

The service is based on PostgreSQL. The database, user, passwords, ownership, connection, server settings, backups,
and imports work as described in the [PostgreSQL guide](https://wodby.com/docs/2.0/stacks/catalog/postgres/).

## PostGIS extensions

Wodby creates these extensions in a database when it creates the database. The application does not run
`CREATE EXTENSION postgis`.

- `postgis`
- `postgis_raster`
- `postgis_sfcgal`
- `fuzzystrmatch`
- `address_standardizer`
- `address_standardizer_data_us`
- `postgis_tiger_geocoder`
- `postgis_topology`

Setting `POSTGRES_DB_EXTENSIONS` on the service replaces this whole list. To add an extension such as `vector`, repeat
the PostGIS extensions you need and append the new one. See
[Extensions](https://wodby.com/docs/2.0/stacks/catalog/postgres/#extensions) in the PostgreSQL guide.

## Check the PostGIS version

Open a [web terminal](https://wodby.com/docs/2.0/apps/web-terminal/) for the service and run:

```
PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -U postgres -d <database> -c 'SELECT postgis_full_version();'

```
