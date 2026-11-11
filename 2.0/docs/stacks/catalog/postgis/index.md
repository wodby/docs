---
description: Run a PostgreSQL database server that bundles PostGIS on Wodby with the PostGIS catalog stack, a single service with a 20 GB data volume.
---

# PostGIS

The Wodby PostGIS catalog stack runs a PostgreSQL database server that bundles PostGIS. The current composition is
documented in [`wodby/stack-postgis`](https://github.com/wodby/stack-postgis). It has one service, with a 20 GB `data`
volume. It has no Adminer or pgAdmin option.

The service is based on PostgreSQL. The database, user, passwords, ownership, connection, server settings, backups,
and imports work as described in the [PostgreSQL guide](../postgres/index.md).

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
[Extensions](../postgres/index.md#extensions) in the PostgreSQL guide.

## Check the PostGIS version

Open a [web terminal](../../../apps/web-terminal.md) for the service and run:

```bash
PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -U postgres -d <database> -c 'SELECT postgis_full_version();'
```
